# %% [Install Dependencies]
# Assuming necessary dependencies like langchain, huggingface, dotenv are installed
# !pip install -qU langchain langchain_huggingface python-dotenv pydantic transformers

# %% [Configuration]
import os
import logging
import warnings
import re
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv
from getpass import getpass

# Load environment variables from .env file if it exists
load_dotenv()

# --- Suppress specific warnings ---
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*'post' (from 'huggingface_hub.inference._client') is deprecated.*")
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub.*")

# --- Configuration Class ---
@dataclass
class RiskToleranceConfig:
    """Configuration for the Risk Tolerance scoring system"""
    model_id: str = "mistralai/Mistral-7B-Instruct-v0.3" # Using the same model as example
    max_attempts: int = 3
    # Define the risk levels with their descriptions and scores
    # Further refinement, esp. for 50
    risk_levels: Dict[int, str] = field(default_factory=lambda: {
        10: "Very low risk taker: Absolute priority is capital protection. Avoids ANY short-term loss or fluctuation. Wants utmost safety.",
        20: "Low risk taker: Prioritizes capital safety but accepts MINIMAL volatility for returns slightly above savings. Dislikes seeing balance go down.",
        30: "Average risk taker: Focuses on preserving capital but accepts SMALL/MINOR short-term dips ('a bit of risk') for MODERATE long-term returns.",
        40: "High risk taker: Seeks GOOD long-term returns and accepts NOTICEABLE/MODERATE negative fluctuations or temporary losses ('moderate swings', 'balance') to achieve them.",
        50: "Very high risk taker: Aims for the HIGHEST possible returns or MAXIMIZING growth potential, understanding and accepting the possibility of SIGNIFICANT short-term losses or market drops.",
    })
    # Store the scores expected from the LLM for validation
    valid_scores: List[int] = field(init=False) # Will be populated from risk_levels keys

    llm_params: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 0.01, # Keep deterministic
        "max_new_tokens": 10, # Shorter output needed (just a number or 'none')
        "top_k": 10,
        "repetition_penalty": 1.2,
    })

    def __post_init__(self):
        # Populate valid_scores after the instance is created
        self.valid_scores = list(self.risk_levels.keys())
        self.num_options = len(self.risk_levels) # Store number of options for checks

# %% [Utility Functions]
# --- Logging Setup ---
def setup_logging(level=logging.INFO) -> logging.Logger:
    """Configure logging for the application"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("httpcore").setLevel(logging.ERROR)
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
    logging.getLogger("transformers").setLevel(logging.ERROR)
    return logging.getLogger("RiskToleranceChatbot")

logger = setup_logging()

# --- API Token Helper (Copied from Stage of Life Chatbot) ---
# (Keeping the robust get_huggingface_token function as before)
def get_huggingface_token() -> Optional[str]:
    hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
    if hf_token:
        logger.info("Hugging Face token found in environment variables.")
        return hf_token
    try:
        # Standard Colab check
        from google.colab import userdata
        hf_token = userdata.get('HUGGINGFACE_API_TOKEN')
        if hf_token:
            logger.info("Hugging Face token found in Colab userdata.")
            return hf_token
    except (ImportError, ModuleNotFoundError):
        logger.debug("google.colab module not found, skipping userdata check.")
    except KeyError:
        logger.info("Hugging Face token not found in Colab userdata.")
    except Exception as e:
        logger.warning(f"An unexpected error occurred while checking Colab userdata: {e}")

    # Check Kaggle secrets if not in Colab
    try:
        from kaggle_secrets import UserSecretsClient
        user_secrets = UserSecretsClient()
        hf_token = user_secrets.get_secret("HUGGINGFACE_API_TOKEN")
        if hf_token:
            logger.info("Hugging Face token found in Kaggle Secrets.")
            return hf_token
        else:
            logger.info("Hugging Face token not found in Kaggle Secrets.")
    except (ImportError, ModuleNotFoundError):
        logger.debug("kaggle_secrets module not found, skipping Kaggle check.")
    except Exception as e: # Catch potential exceptions from get_secret
        logger.warning(f"Could not retrieve token from Kaggle Secrets: {e}")

    logger.warning("Hugging Face token not found in environment, Colab userdata, or Kaggle Secrets.")
    print("Please enter your Hugging Face API token (needed for the LLM):")
    try:
        hf_token = getpass("    > ")
        if hf_token:
            logger.info("Hugging Face token received via prompt.")
            print("Tip: Set the HUGGINGFACE_API_TOKEN environment variable (or use Colab/Kaggle secrets) for automatic use next time.")
            return hf_token
        else:
            logger.error("No Hugging Face token provided via prompt.")
            return None
    except EOFError:
         logger.error("Could not read Hugging Face token from input (EOF encountered).")
         return None
    except Exception as e:
         logger.error(f"An error occurred while getting token from prompt: {e}")
         return None

# %% [LLM Setup]
def setup_llm_chain(config: RiskToleranceConfig):
    """Sets up the LangChain LLM chain for risk tolerance identification."""
    from langchain_huggingface import HuggingFaceEndpoint
    from langchain.chains import LLMChain
    from langchain_core.prompts import PromptTemplate

    hf_token = get_huggingface_token()
    if not hf_token:
        raise ValueError("Hugging Face API token is required but could not be obtained.")

    try:
        llm = HuggingFaceEndpoint(
            repo_id=config.model_id,
            task="text-generation",
            huggingfacehub_api_token=hf_token,
            **config.llm_params
        )
    except Exception as e:
        logger.exception(f"Failed to initialize HuggingFaceEndpoint for model {config.model_id}: {e}")
        raise ConnectionError(f"Could not connect to Hugging Face Endpoint: {e}") from e

    # --- Build the prompt dynamically from the config ---
    options_text = ""
    # Ensure consistent ordering for prompt generation
    sorted_scores = sorted(config.risk_levels.keys())
    option_map = {idx + 1: score for idx, score in enumerate(sorted_scores)}

    for score in sorted_scores:
         description = config.risk_levels[score]
         # Extract core description for prompt clarity
         desc_part = description.split(":", 1)[1].strip() if ":" in description else description
         # Add emphasis for key differentiating terms if helpful
         desc_part = desc_part.replace("ANY", "**ANY**").replace("MINIMAL", "**MINIMAL**").replace("SMALL/MINOR", "**SMALL/MINOR**").replace("NOTICEABLE/MODERATE", "**NOTICEABLE/MODERATE**").replace("HIGHEST", "**HIGHEST**").replace("MAXIMIZING", "**MAXIMIZING**").replace("SIGNIFICANT", "**SIGNIFICANT**")
         options_text += f"  - {score} -> Matches: \"{desc_part}\"\n"

    # --- Final Refined Prompt Template ---
    risk_tolerance_template = f"""You are an AI assistant specialized in classifying user statements about investment risk tolerance into ONE of five predefined categories based on their expressed attitude towards risk, return, capital preservation, and fluctuation tolerance.

**Your Task:**
1.  Analyze the user's input statement carefully. Pay attention to keywords indicating risk aversion, risk tolerance, return goals, and acceptance of potential losses or fluctuations.
2.  Determine which single predefined risk category **best** matches the user's overall sentiment.
3.  Respond with **ONLY** the single numeric score corresponding to the chosen category.
4.  If the input is irrelevant, clearly ambiguous, contradictory, expresses no preference, or doesn't provide enough information to fit into any single category, respond with the single word **none**.

**Predefined Categories and Matching Criteria:**
{options_text}
  - none -> Use this category if the input:
    *   Is non-contextual (e.g., hobbies unrelated to investment goals, unrelated questions).
    *   Is excessively vague (e.g., "I want to invest", "What should I do?").
    *   Expresses clear uncertainty or inability to choose (e.g., "not sure", "maybe", "I don't know").
    *   Is inherently contradictory without resolution (e.g., "Maximum returns with zero risk", "Good returns but totally safe").
    *   Focuses *only* on factors like time horizon ("long term") or general asset types ("I like equities/bonds") without indicating *personal tolerance* for risk/fluctuation.
    *   Is an invalid number (not 1-{config.num_options} or {', '.join(map(str, config.valid_scores))}).

**Input Interpretation Rules:**
1.  **Numeric Input:** Handled by the system *before* you see it if it's 1-{config.num_options} or an invalid number. You might receive an input that is one of the exact score numbers ({', '.join(map(str, config.valid_scores))}); in that case, output that number.
2.  **Descriptive Input:**
    *   **Keywords:** Look for terms related to: safety, protection, loss aversion, stability, fluctuation, volatility, dips, swings, growth, returns, potential, maximizing.
    *   **Sentiment:** Assess the overall feeling - cautious, balanced, aggressive?
    *   **Score 50 Clarification:** Statements strongly emphasizing **maximizing growth potential** or aiming for the **highest returns** (e.g., "Maximize my growth potential!", "Go for max growth!", "Highest returns possible") should be classified as 50, *even if loss tolerance isn't explicitly detailed*, unless the statement includes contradictory elements strongly prioritizing safety. Ignore simple formatting (like emojis) or unrelated distractions (like hobbies mentioned alongside the goal).
    *   **Vague Growth/Safety:** Statements like "I want my money to grow" or "I want safe investments", *without further qualification* about fluctuation tolerance or return expectations relative to risk, are too vague and should be classified as `none`. Contrast with "Maximize growth" (Score 50) or "Absolute safety" (Score 10).
    *   **Distinguish 30 vs 40:** Score 30 accepts only 'small/minor' risk/dips. Score 40 accepts 'moderate/noticeable' fluctuations/swings for 'good' returns (often implying a balance).
    *   **Figurative Language:** Interpret common idioms (e.g., "don't want to lose my shirt" -> strong aversion, likely 10).
    *   **Comparisons:** Interpret relative statements (e.g., "More risk than savings, less than stocks" likely points to 20 or 30).

**CRITICAL OUTPUT FORMAT:**
Your entire response MUST be **EITHER** one of the numeric scores ({', '.join(map(str, config.valid_scores))}) **OR** the exact word `none`.
ABSOLUTELY NO other text, explanation, punctuation, apologies, or formatting. Just the number or 'none'.

**Examples:**
- Input: "30" -> Output: 30
- Input: "6" -> Output: none (Handled by system, but illustrative)
- Input: "Maximize my growth potential! That's the main goal." -> Output: 50
- Input: "I enjoy gardening and want to maximize my growth potential with investments." -> Output: 50
- Input: "Go for max growth! 🚀" -> Output: 50
- Input: "I want my money to grow." -> Output: none
- Input: "Growth." -> Output: none
- Input: "I want safe investments." -> Output: none
- Input: "I want good returns, but also want it to be safe." -> Output: none
- Input: "Maximum possible returns with absolutely zero risk." -> Output: none
- Input: "Keep it mostly safe, but I don't mind tiny risks for a bit more interest." -> Output: 20 (or 30 depending on interpretation of 'tiny')
- Input: "Willing to accept moderate fluctuations for better potential returns than just keeping capital." -> Output: 40
- Input: "I prefer equities." -> Output: none
- Input: "Bonds seem good." -> Output: none (Preference for asset class is not risk tolerance)
- Input: "Quiero proteger mi capital." -> Output: 10
- Input: "I don't want to lose my shirt in the market." -> Output: 10
- Input: "More risk than just savings, less than pure stocks." -> Output: 30

User Input: {{user_input}}
AI Output:"""

    prompt = PromptTemplate(template=risk_tolerance_template, input_variables=["user_input"])

    try:
        risk_chain = LLMChain(prompt=prompt, llm=llm, verbose=False)
        logger.info(f"LLM Chain initialized successfully for Risk Tolerance with model {config.model_id}.")
        return risk_chain
    except Exception as e:
        logger.exception(f"Failed to create LLMChain for Risk Tolerance: {e}")
        raise RuntimeError(f"Could not create Risk Tolerance LLMChain: {e}") from e


# %% [Main Application Class]
class RiskToleranceChatbot:
    """Manages the risk tolerance query, LLM interaction, parsing, and scoring."""

    def __init__(self, config: Optional[RiskToleranceConfig] = None):
        """Initializes the chatbot with configuration."""
        self.config = config or RiskToleranceConfig()
        self._llm_chain = None
        self._llm_initialized = False
        # Ensure consistent ordering by sorting keys before creating the map
        sorted_scores = sorted(self.config.risk_levels.keys())
        self.option_to_score_map = {
            idx + 1: score for idx, score in enumerate(sorted_scores)
        }
        # Create reverse map for displaying description using the potentially updated config descriptions
        self.score_to_description_map = self.config.risk_levels

        logger.info("RiskToleranceChatbot initialized.")
        logger.debug(f"Configuration: {self.config}")
        logger.debug(f"Option to Score Map: {self.option_to_score_map}")


    def _initialize_llm_chain(self):
        """Initializes the LLM chain if not already done."""
        if not self._llm_initialized:
            logger.info("Attempting to initialize LLM chain for Risk Tolerance...")
            try:
                self._llm_chain = setup_llm_chain(self.config)
                self._llm_initialized = True
            except (ValueError, ConnectionError, RuntimeError) as e:
                logger.error(f"Risk Tolerance LLM Chain initialization failed: {e}")
                raise # Propagate the error

    @property
    def llm_chain(self):
        """Property to lazily initialize and return the LLM chain."""
        if not self._llm_initialized:
            self._initialize_llm_chain()
        if not self._llm_chain:
            raise RuntimeError("Risk Tolerance LLM Chain could not be initialized.")
        return self._llm_chain

    def parse_llm_risk_response(self, llm_text_output: str) -> Optional[int]:
        """
        Parses the LLM's text output expecting a risk score number or 'none'.
        Returns the integer score or None if 'none' or parsing fails.
        Handles potential noise more robustly.
        """
        # Remove potential markdown/formatting artifacts before stripping
        cleaned_output = re.sub(r"[`\*_]", "", llm_text_output)
        cleaned_output = cleaned_output.strip().lower()
        logger.debug(f"Attempting to parse LLM risk response: '{cleaned_output}'")

        # Direct match for 'none'
        if cleaned_output == "none":
            logger.info("LLM indicated no matching risk category ('none').")
            return None

        # Try to extract numbers using regex
        numbers_found = re.findall(r'\d+', cleaned_output)

        # Ideal case: Exactly one number found and it's the entire cleaned string
        if len(numbers_found) == 1 and numbers_found[0] == cleaned_output:
            try:
                score = int(numbers_found[0])
                if score in self.config.valid_scores:
                    logger.info(f"Successfully parsed exact risk score from LLM: {score}")
                    return score
                else:
                    logger.warning(f"Parsed number {score} is not a valid risk score: {self.config.valid_scores}. Treating as invalid. Raw Output: '{llm_text_output}'")
                    return None
            except ValueError:
                 logger.error(f"Regex found digits but failed conversion? '{cleaned_output}'")
                 return None

        # Fallback: If there's noise but exactly one valid score number is present
        elif len(numbers_found) == 1:
             try:
                 potential_score = int(numbers_found[0])
                 if potential_score in self.config.valid_scores:
                     logger.warning(f"Extracted the only valid score ({potential_score}) from noisy LLM output: '{llm_text_output}'. Assuming this is the intended output.")
                     return potential_score
                 else:
                     logger.warning(f"Extracted number {potential_score} from noisy output, but it's not a valid score. Raw: '{llm_text_output}'")
                     return None
             except ValueError:
                  logger.error(f"Regex found digits but failed conversion in noisy output? '{cleaned_output}'")
                  return None

        # Handle cases where multiple numbers or no numbers are found, or it's non-'none' text
        logger.error(f"Failed to parse LLM risk response: '{llm_text_output}'. Expected one of {self.config.valid_scores} or 'none'. Found numbers: {numbers_found}")
        return None # Indicate parsing failure


    def process_user_input(self, user_input: str) -> Optional[int]:
        """
        Processes user input. Handles direct numeric input (1-N) and invalid numbers
        before potentially sending to the LLM for description analysis.
        Returns the integer score or None if processing fails or LLM returns 'none'.
        """
        if not user_input:
            logger.warning("Received empty user input.")
            return None

        # --- Pre-LLM Check for Numeric Input ---
        cleaned_numeric_input = user_input.strip()
        try:
            num_input = int(cleaned_numeric_input)
            # Check if it's a valid option number (1 to num_options)
            if num_input in self.option_to_score_map:
                score = self.option_to_score_map[num_input]
                logger.info(f"Detected direct option number '{num_input}', mapped to score: {score}")
                return score
            # Check if it's one of the exact valid scores (e.g., 10, 20, ...)
            elif num_input in self.config.valid_scores:
                 logger.info(f"Detected direct score input '{num_input}'. Using this score.")
                 return num_input
            # Check if it's *any other number* -> Invalid
            else:
                logger.warning(f"Numeric input '{num_input}' is not a valid option (1-{self.config.num_options}) or a valid score ({self.config.valid_scores}). Treating as invalid input.")
                return None
        except ValueError:
            # Not a simple integer, likely a description, proceed to LLM
            logger.debug(f"Input '{user_input}' is not purely numeric, passing to LLM for analysis.")
            pass
        # --- End Pre-LLM Check ---


        llm_error_msg = "" # To track specific communication errors
        try:
            llm_chain_instance = self.llm_chain # Trigger initialization if needed
            # Pass the original user input, not the potentially cleaned one for numeric checks
            logger.info(f"Sending user input to Risk Tolerance LLM: '{user_input}'")
            llm_response = llm_chain_instance.invoke({"user_input": user_input})

            # Extract text output robustly
            if isinstance(llm_response, dict):
                llm_text_output = llm_response.get('text', '')
            elif isinstance(llm_response, str):
                llm_text_output = llm_response
            else:
                llm_text_output = str(llm_response) # Fallback

            # llm_text_output = llm_text_output.strip() # Stripping happens in parse function now

            if not llm_text_output: # Check if response exists before parsing
                logger.error("Received empty response from Risk Tolerance LLM.")
                return None
            logger.info(f"Received Risk Tolerance LLM response: '{llm_text_output}'")

            # Parse the LLM response
            parsed_score = self.parse_llm_risk_response(llm_text_output) # Handles stripping and parsing

            if parsed_score is not None:
                logger.info(f"Successfully processed risk input via LLM. Derived score: {parsed_score}.")
                return parsed_score
            else:
                logger.warning(f"Risk Tolerance LLM response ('{llm_text_output}') did not yield a valid score or was 'none'.")
                return None # Indicate failure or 'none' case

        except (ValueError, ConnectionError, RuntimeError) as llm_error:
             llm_error_msg = f"LLM-related error during risk tolerance processing: {llm_error}"
             logger.error(llm_error_msg)
             self.last_llm_error = llm_error_msg # Store for interaction loop
             print(f"\n[Error] Sorry, there was a problem communicating with the analysis service.")
             return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred during risk tolerance LLM interaction or processing: {e}")
            print(f"\n[Error] An unexpected issue occurred: {e}")
            return None
        finally:
             if 'llm_error_msg' not in locals() or not llm_error_msg:
                 if hasattr(self, 'last_llm_error'):
                     delattr(self, 'last_llm_error')


    def run_interaction(self):
        """Runs the interactive command-line loop for the risk tolerance chatbot."""
        print("\n" + "="*45)
        print(" Investment Objective & Risk Tolerance")
        print("="*45)
        print("\nLet's determine the score for your risk tolerance.")

        # Display options clearly using the chatbot's maps
        print("\nWhich statement best describes your investment objective and risk tolerance?")
        print(f"You can enter the corresponding number (1-{self.config.num_options}) or describe your situation in your own words:")
        for option_num, score in self.option_to_score_map.items():
            description = self.score_to_description_map.get(score, "Unknown description")
            desc_parts = description.split(":")
            desc_title = desc_parts[0].strip() if len(desc_parts) > 0 else ""
            desc_detail = desc_parts[1].strip() if len(desc_parts) > 1 else description
            print(f"{option_num}. {desc_title}. ({desc_detail}) (Score: {score})")

        attempts = 0
        final_score = None
        self.last_llm_error = None # Reset last error attribute

        try:
            # Initialize LLM early
            self._initialize_llm_chain()
        except (ValueError, ConnectionError, RuntimeError, Exception) as init_error:
            print(f"\n[Critical Error] Sorry, I couldn't set up the analysis system: {init_error}")
            print("Please check your setup (API token, network) and try again later.")
            return None

        while attempts < self.config.max_attempts:
            current_attempt = attempts + 1
            try:
                if attempts == 0:
                    prompt_message = f"Please enter the option number (1-{self.config.num_options}) or describe your approach:"
                else:
                    prompt_message = "Let's try again. Please enter the option number or describe your approach:"

                print(f"\n[{current_attempt}/{self.config.max_attempts}] {prompt_message}")
                user_input = input("    > ").strip()

                if not user_input:
                    print("Whoops, looks like you didn't type anything. Please provide an answer.")
                    continue

                # Process the input (includes pre-LLM checks)
                score_result = self.process_user_input(user_input)

                if score_result is not None:
                    # Successfully got a score
                    selected_description = self.score_to_description_map.get(score_result, "Unknown category")
                    print(f"\nUnderstood! Based on your input, the closest match is:")
                    print(f"  '{selected_description}'")
                    print(f"The score for this risk level is: {score_result}")
                    final_score = score_result
                    break # Success!
                else:
                    # process_user_input returned None
                    print("\nHmm, I wasn't able to determine a matching risk level from that.")
                    if not hasattr(self, 'last_llm_error') or self.last_llm_error is None:
                         # Check if it was rejected pre-LLM as invalid number
                         is_numeric_invalid = False
                         try:
                             num = int(user_input.strip())
                             if num not in self.option_to_score_map and num not in self.config.valid_scores:
                                 is_numeric_invalid = True
                         except ValueError:
                             pass # Not numeric

                         if not is_numeric_invalid:
                            print("Could you try rephrasing, providing more detail, or selecting the option number?")

                    self.last_llm_error = None # Reset error flag
                    attempts += 1 # Increment attempts on failure

            except KeyboardInterrupt:
                print("\n\nOkay, cancelling this assessment.")
                return None
            except EOFError:
                print("\n\nInput ended unexpectedly.")
                return None
            except Exception as e:
                 logger.exception(f"An unexpected error occurred in the interaction loop: {e}")
                 print(f"\nAn unexpected issue occurred ({type(e).__name__}). Let's try that again.")
                 attempts += 1

        # After the loop
        if final_score is None and attempts >= self.config.max_attempts:
             print("\nSorry, I couldn't determine the risk tolerance score after a few tries.")
             print("We may need to skip this question.")

        return final_score

# %% [Main Execution]
if __name__ == "__main__":
    chatbot_instance = None
    final_result = None
    try:
        app_config = RiskToleranceConfig()
        chatbot_instance = RiskToleranceChatbot(config=app_config)
        final_result = chatbot_instance.run_interaction()

        if final_result is not None:
            print(f"\n--- Risk Tolerance Assessment Complete. Final Score: {final_result} ---")
        else:
            print("\n--- Risk Tolerance Assessment ended without determining a final score. ---")

    except Exception as main_error:
         logger.exception(f"A critical error occurred in the main execution block: {main_error}")
         print(f"\nA critical error occurred during setup or execution: {main_error}")

    finally:
        print("\nExiting Risk Tolerance Assessment.")