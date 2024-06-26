from emotion_detective.models.model_definitions import load_model
import torch
from transformers import RobertaTokenizerFast, BertTokenizer
from datasets import Dataset
from torch.utils.data import DataLoader, TensorDataset
import logging
import json

# Assuming you have a logger already configured
logger = logging.getLogger(__name__)


def get_predictions(model_path, df, emotion_mapping_path=None, model_type='roberta'):
    """
    Perform predictions using a specified model on a DataFrame containing text data.
    This function loads a model, tokenizes input data based on the specified model_type,
    performs predictions, and optionally maps numeric emotions back to string labels.

    Parameters:
    - model_path (str): Path to the trained model.
    - df (pd.DataFrame): DataFrame containing 'text' column with input text data.
    - emotion_mapping_path (str, optional): Path to JSON file mapping numeric emotions 
    to string labels.
    - model_type (str, optional): Type of model to use ('roberta' or 'rnn'). Default is
    'roberta'.

    Returns:
    pd.DataFrame: DataFrame with added 'emotion' column containing predicted emotions.

    Raises:
    ValueError: If an unsupported model_type is provided.
    Exception: If there's an error during tokenization, prediction, or emotion mapping.

    Author: Rebecca Borski
    """
    logger.info("Starting predictions...")

    if model_type == 'roberta':
        logger.debug("Using Roberta model")
        # Load tokenizer
        tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base', max_length=512)

        # Tokenize the data
        def tokenize(batched_text):
            return tokenizer(batched_text['text'], padding=True, truncation=True)

        # Map the tokenization function to your DataFrame
        tokenized_data = Dataset.from_pandas(df).map(tokenize, batched=True)

        # Set format to torch tensors
        tokenized_data.set_format('torch', columns=['input_ids', 'attention_mask'])

        # Prepare DataLoader
        dataloader = torch.utils.data.DataLoader(tokenized_data, batch_size=8)

    elif model_type == 'rnn':
        logger.debug("Using RNN model")
        # Initialize the tokenizer
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

        # Tokenization function
        def tokenize(text):
            return tokenizer.encode(text, max_length=512, truncation=True,
                                    padding='max_length')

        # Tokenize data
        df['input_ids'] = df['text'].apply(lambda x: tokenize(x))

        # Prepare DataLoader
        dataset = TensorDataset(
            torch.tensor(df['input_ids'].tolist())
        )
        dataloader = DataLoader(dataset, batch_size=8)

    else:
        logger.debug(f"Unsupported model_type: {model_type} use rnn or roberta")
        raise ValueError(f"Unsupported model_type: {model_type}")

    # Load model
    model = load_model(model_path)

    # Put model in evaluation mode
    model.eval()

    # Empty lists to store predictions
    predictions = []

    # Predict
    with torch.no_grad():
        for batch in dataloader:
            try:
                if model_type == 'roberta':
                    input_ids = batch['input_ids'].to(
                        'cuda' if torch.cuda.is_available() else 'cpu')
                    attention_mask = batch['attention_mask'].to(
                        'cuda' if torch.cuda.is_available() else 'cpu')
                    outputs = model(input_ids, attention_mask=attention_mask)
                    logits = outputs.logits
                elif model_type == 'rnn':
                    input_ids = batch[0].to('cpu')
                    outputs = model(input_ids)
                    logits = outputs
                else:
                    continue

                # Get predicted class
                preds = torch.argmax(logits, dim=-1)

                # Append predictions to list
                predictions.extend(preds.cpu().numpy())

            except Exception as e:
                logger.error(f"Error in get_predictions: {e}")
                raise e

    # Add predictions to dataframe
    df['emotion'] = predictions

    # Load and map the emotions back to string labels if emotion_mapping_path is True
    if emotion_mapping_path is not None:
        try:
            with open(emotion_mapping_path, 'r') as f:
                emotion_mapping = json.load(f)
            inverse_emotion_mapping = {v: k for k, v in emotion_mapping.items()}
            df['emotion'] = df['emotion'].map(inverse_emotion_mapping)
        except Exception as e:
            logger.error(f"Error loading or processing emotion mapping: {e}")
            raise e

    logger.info("Predictions completed.")
    return df
