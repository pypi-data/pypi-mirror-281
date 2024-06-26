import typer
from colorama import Fore, Style
from emotion_detective.logger.logger import setup_logging
from emotion_detective.data.training.data_ingestion import load_data
from emotion_detective.data.training.data_preprocessing import (
    balancing_multiple_classes, preprocess_text
)
from emotion_detective.models.model_saving import save_model
from emotion_detective.models.model_training import (
    train_and_evaluate_rnn, train_and_evaluate_roberta
)
from emotion_detective.models.model_definitions import roberta_model, rnn_model

app = typer.Typer()


def show_instructions():
    instructions = (
        f"{Fore.YELLOW}🎭 Welcome to the Emotion Classifier Training CLI! "
        f"🎭{Style.RESET_ALL}\n\n"
        f"{Fore.CYAN}This tool trains a classification model to detect emotions "
        f"from text data. {Style.RESET_ALL}\n\n"
        f"{Fore.GREEN}🚀 Instructions: {Style.RESET_ALL}\n"
        f"1. {Fore.BLUE}train_data_path: {Style.RESET_ALL} Path to the file "
        f"containing the training data. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"2. {Fore.BLUE}test_data_path: {Style.RESET_ALL} Path to the file "
        f"containing the testing data. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"3. {Fore.BLUE}text_column: {Style.RESET_ALL} Name of the column in the "
        f"DataFrame containing text data. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"4. {Fore.BLUE}emotion_column: {Style.RESET_ALL} Name of the column in the"
        f"DataFrame containing emotion labels. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"5. {Fore.BLUE}num_epochs: {Style.RESET_ALL} Number of epochs to train the "
        f"model. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"6. {Fore.BLUE}model_type: {Style.RESET_ALL} Type of model that is going to "
        f"be used (roberta, rnn) {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"7. {Fore.BLUE}model_dir: {Style.RESET_ALL} Directory where the trained model "
        f"will be saved. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"8. {Fore.BLUE}model_name: {Style.RESET_ALL} Name to use when saving the "
        f"trained model. {Fore.RED}[required]{Style.RESET_ALL}\n"
        f"9. {Fore.BLUE}learning_rate: {Style.RESET_ALL} Learning rate for the "
        f"optimizer. {Fore.RED}[optional, defaults to 0.001]{Style.RESET_ALL}\n"
        f"10. {Fore.BLUE}train_batch_size: {Style.RESET_ALL} Batch size for training. "
        f"{Fore.RED}[optional, defaults to 4]{Style.RESET_ALL}\n"
        f"11. {Fore.BLUE}eval_batch_size: {Style.RESET_ALL} Batch size for evaluation. "
        f"{Fore.RED}[optional, defaults to 8]{Style.RESET_ALL}\n"
        f"12. {Fore.BLUE}cloud_logging: {Style.RESET_ALL} Set to 'True', if you "
        f"are using AzureML cloud services. {Fore.RED}"
        f" [optional, defaults to True]{Style.RESET_ALL}\n\n"
        f"{Fore.MAGENTA}🔔 Please provide the necessary inputs when prompted."
        f"🔔{Style.RESET_ALL}\n"
    )
    print(instructions)


def training_pipeline(
    train_data_path: str,
    test_data_path: str,
    text_column: str,
    emotion_column: str,
    num_epochs: int,
    model_type: str,
    model_dir: str,
    model_name: str,
    learning_rate: float = 0.001,
    train_batch_size: int = 4,
    eval_batch_size: int = 8,
    cloud_logging: bool = True
):
    logger = setup_logging()

    try:
        # Load data
        logger.info("Loading data...")
        train_data = load_data(train_data_path, text_column, emotion_column)
        test_data = load_data(test_data_path, text_column, emotion_column)

        # Preprocess text
        logger.info("Preprocessing text...")
        train_data = preprocess_text(train_data)
        test_data = preprocess_text(test_data)

        # Balance classes
        logger.info("Balancing classes...")
        train_data = balancing_multiple_classes(train_data)

        NUM_LABELS = train_data['label'].nunique()

        if model_type == 'roberta':
            model = roberta_model(NUM_LABELS)
            # Train and evaluate model
            logger.info("Training and evaluating model...")
            trained_model, eval = train_and_evaluate_roberta(
                model, train_data, test_data, num_train_epochs=num_epochs,
                learning_rate=learning_rate, eval_batch_size=eval_batch_size,
                train_batch_size=train_batch_size, cloud_logging=cloud_logging
            )
        if model_type == 'rnn':
            model = rnn_model(NUM_LABELS)
            # Train and evaluate model
            logger.info("Training and evaluating model...")
            trained_model = train_and_evaluate_rnn(
                model, train_data, test_data, num_epochs=num_epochs,
                learning_rate=learning_rate, eval_batch_size=eval_batch_size,
                train_batch_size=train_batch_size, cloud_logging=cloud_logging
            )
        # Save model
        logger.info("Saving model...")
        save_model(trained_model, model_dir, model_name)

        logger.info("Training pipeline completed successfully.")

    except Exception as e:
        logger.error(f"Error in training pipeline: {e}")
        raise


@app.command()
def train(
    train_data_path: str = typer.Option(
        None, help="Path to the file containing the training data"
    ),
    test_data_path: str = typer.Option(
        None, help="Path to the file containing the testing data"
    ),
    text_column: str = typer.Option(
        None, help="Name of the column in the DataFrame containing text data"
    ),
    emotion_column: str = typer.Option(
        None, help="Name of the column in the DataFrame containing emotion labels"
    ),
    num_epochs: int = typer.Option(
        None, help="Number of epochs to train the model"
    ),
    model_type: str = typer.Option(
        None, help="Type of model that is going to be used (roberta, rnn)"
    ),
    model_dir: str = typer.Option(
        None, help="Directory where the trained model will be saved"
    ),
    model_name: str = typer.Option(
        None, help="Name to use when saving the trained model"
    ),
    learning_rate: float = typer.Option(
        0.001, help="Learning rate for the optimizer"
    ),
    train_batch_size: int = typer.Option(
        4, help="Batch size for training"
    ),
    eval_batch_size: int = typer.Option(
        8, help="Batch size for evaluation"
    ),
    cloud_logging: bool = typer.Option(
        True, help="Set to 'True' if you are using AzureML cloud services"
    )

):
    show_instructions()
    train_data_path = input("Enter training file path: ")
    test_data_path = input("Enter testing file path: ")
    text_column = input("Enter text column name: ")
    emotion_column = input("Enter emotion column name: ")
    num_epochs = int(input("Enter number of epochs: "))
    model_type = str(input("Enter model type: "))
    model_dir = input("Enter model directory: ")
    model_name = input("Enter model name: ")
    learning_rate = float(input("Enter learning rate: (press Enter for default)"))
    train_batch_size = int(input("Enter train batch size: (press Enter for default)"))
    eval_batch_size = int(input("Enter eval batch size: (press Enter for default)"))
    cloud_logging = input("Enable cloud logging: (press Enter for default)")

    training_pipeline(
        train_data_path,
        test_data_path,
        text_column,
        emotion_column,
        num_epochs,
        model_type,
        model_dir,
        model_name,
        learning_rate,
        train_batch_size,
        eval_batch_size,
        cloud_logging
        )


if __name__ == "__main__":
    app()
