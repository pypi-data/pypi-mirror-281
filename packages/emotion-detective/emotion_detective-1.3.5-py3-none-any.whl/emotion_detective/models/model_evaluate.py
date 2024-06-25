import logging
import os
import json
import torch
import pandas as pd
from transformers import Trainer, RobertaTokenizerFast, TrainingArguments
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from typing import Any, Dict
from datasets import Dataset
import torch.nn as nn
import typer
from torch.utils.data import DataLoader, TensorDataset
from transformers import BertTokenizer

# Logger setup
logger = logging.getLogger(__name__)


def validate_labels(test_data: pd.DataFrame, num_classes: int) -> None:
    """
    Validate that the labels in the test data are within the expected range.

    Parameters:
    test_data (pd.DataFrame): DataFrame containing the test data with a 'label' column.
    num_classes (int): Number of classes expected.

    Raises:
    AssertionError: If any label is out of the expected range.

    Author: Andrea Tosheva
    """
    assert test_data['label'].max() < num_classes, (
        f"Label value {test_data['label'].max()} is out of bounds." 
        f"Expected less than {num_classes}." )
    assert test_data['label'].min() >= 0, \
        "Label value should be non-negative."


def evaluate_model(
    model: nn.Module,
    test_data: pd.DataFrame,
    model_type: str,
    output_dir: str = './',
    logging_dir: str = './',
    eval_batch_size: int = 8,
    disable_tqdm: bool = False,
    dataloader_num_workers: int = 8,
    seed: int = 42,
    num_classes: int = 6
) -> Dict[str, Any]:
    """
    Evaluate the model based on its type (RoBERTa or RNN).

    Parameters:
    model (nn.Module): The model to be evaluated.
    test_data (pd.DataFrame): DataFrame containing the test data.
    model_type (str): Type of the model ('roberta' or 'rnn').
    output_dir (str): Directory to save the evaluation results.
    logging_dir (str): Directory to save the logs.
    eval_batch_size (int): Batch size for evaluation.
    disable_tqdm (bool): Whether to disable the progress bar.
    dataloader_num_workers (int): Number of subprocesses to use for data loading.
    seed (int): Random seed.
    num_classes (int): Number of classes for classification.

    Returns:
    Dict[str, Any]: Evaluation results.

    Raises:
    ValueError: If an invalid model type is provided.

    Author: Andrea Tosheva
    """
    if model_type == 'roberta':
        return evaluate_roberta(model, test_data, output_dir, logging_dir,
                                eval_batch_size, disable_tqdm, dataloader_num_workers, seed, num_classes)
    elif model_type == 'rnn':
        return evaluate_rnn(model, test_data, output_dir, eval_batch_size)
    else:
        raise ValueError("Invalid model type. Please choose 'roberta' or 'rnn'.")


def evaluate_roberta(
    roberta_model: nn.Module,
    test_data: pd.DataFrame,
    output_dir: str = './',
    logging_dir: str = './',
    eval_batch_size: int = 8,
    disable_tqdm: bool = False,
    dataloader_num_workers: int = 8,
    seed: int = 42,
    num_classes: int = 6
) -> Dict[str, Any]:
    """
    Evaluate a RoBERTa model on test data.

    Parameters:
    roberta_model (nn.Module): The RoBERTa model to be evaluated.
    test_data (pd.DataFrame): DataFrame containing the test data.
    output_dir (str): Directory to save the evaluation results.
    logging_dir (str): Directory to save the logs.
    eval_batch_size (int): Batch size for evaluation.
    disable_tqdm (bool): Whether to disable the progress bar.
    dataloader_num_workers (int): Number of subprocesses to use for data loading.
    seed (int): Random seed.
    num_classes (int): Number of classes for classification.

    Returns:
    Dict[str, Any]: Evaluation results.

    Author: Andrea Tosheva
    """
    logger.info("Validating labels...")
    validate_labels(test_data, num_classes)

    logger.info("Initializing RoBERTa tokenizer...")
    tokenizer = RobertaTokenizerFast.from_pretrained('roberta-base', max_length=512)

    def tokenization(batched_text: Dict[str, Any]) -> Dict[str, Any]:
        return tokenizer(batched_text['text'], padding=True, truncation=True)

    logger.info("Tokenizing test data...")
    tokenized_test_data = Dataset.from_pandas(test_data).map(
        tokenization, batched=True, batch_size=len(test_data)
    )

    logger.info("Setting format of tokenized test data...")
    tokenized_test_data.set_format(type='torch', columns=['input_ids', 'attention_mask', 'label'])

    def compute_metrics(pred: Any) -> Dict[str, float]:
        labels = pred.label_ids
        preds = pred.predictions.argmax(-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='micro')
        acc = accuracy_score(labels, preds)
        return {
            'accuracy': acc,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }

    logger.info("Setting training arguments")
    eval_args = TrainingArguments(
        output_dir=output_dir,
        evaluation_strategy='epoch',
        save_strategy='epoch',
        logging_dir=logging_dir,
        per_device_eval_batch_size=eval_batch_size,
        logging_steps=10,
        disable_tqdm=disable_tqdm,
        dataloader_num_workers=dataloader_num_workers,
        seed=seed,
        report_to=[],
        metric_for_best_model='eval_loss'
    )

    logger.info("Creating Trainer for evaluation...")
    eval_trainer = Trainer(
        model=roberta_model,
        args=eval_args,
        eval_dataset=tokenized_test_data,
        compute_metrics=compute_metrics
    )

    logger.info("Evaluating model...")
    eval_results = eval_trainer.evaluate()

    logger.info("Saving evaluation results...")
    with open(os.path.join(output_dir, 'evaluation_results_Roberta.json'), 'w') as f:
        json.dump(eval_results, f)

    return eval_results


def evaluate_rnn(
    rnn_model: nn.Module,
    test_data: pd.DataFrame,
    output_dir: str = './',
    eval_batch_size: int = 8,
) -> Dict[str, Any]:
    """
    Evaluate an RNN model on test data.

    Parameters:
    rnn_model (nn.Module): The RNN model to be evaluated.
    test_data (pd.DataFrame): DataFrame containing the test data.
    output_dir (str): Directory to save the evaluation results.
    eval_batch_size (int): Batch size for evaluation.

    Returns:
    Dict[str, Any]: Evaluation results.

    Author: Andrea Tosheva
    """
    logger = logging.getLogger(__name__)

    logger.info("Tokenizing test data...")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    logger.info("Creating tokenization function.")
    def tokenize(text: str, tokenizer: BertTokenizer, max_len: int = 512) -> torch.Tensor:
        return tokenizer.encode(text, max_length=max_len, truncation=True, padding='max_length')

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f"Using {device} device.")

    logger.info("Tokenizing test data.")
    test_data['input_ids'] = test_data['text'].apply(lambda x: tokenize(x, tokenizer))

    logger.info("Creating TensorDataset.")
    test_dataset = TensorDataset(
        torch.tensor(test_data['input_ids'].tolist()),
        torch.tensor(test_data['label'].tolist())
    )

    logger.info("Creating DataLoader.")
    test_loader = DataLoader(test_dataset, batch_size=eval_batch_size, shuffle=False)

    criterion = nn.CrossEntropyLoss()

    logger.info("Evaluating model.")
    rnn_model.eval()
    eval_loss = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        logger.info("Iterating over test data.")
        for inputs, labels in test_loader:
            logger.info("Moving inputs and labels to device.")
            inputs, labels = inputs.to(device), labels.to(device)
            logger.info("Getting model outputs.")
            outputs = rnn_model(inputs)
            loss = criterion(outputs, labels)
            eval_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    logger.info("Calculating evaluation metrics.")
    eval_loss /= len(test_loader)

    logger.info("Calculating evaluation metrics.")
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average='weighted', zero_division=1
    )

    evaluation_results = {
        'eval_loss': eval_loss,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }
    logger.info("Saving evaluation results.")
    with open(os.path.join(output_dir, 'evaluation_results_RNN.json'), 'w') as f:
        json.dump(evaluation_results, f)

    return evaluation_results

# Typer app for CLI
app = typer.Typer()


@app.command()
def evaluate(
    model_path: str = typer.Option(..., help="Path to the trained model file."),
    test_data_path: str = typer.Option(..., help="Path to the test data CSV file."),
    model_type: str = typer.Option(..., help="Type of the model (roberta or rnn)."),
    output_dir: str = typer.Option('./', help="Directory to save the evaluation results."),
    logging_dir: str = typer.Option('./', help="Directory to save the logs."),
    eval_batch_size: int = typer.Option(8, help="Batch size for evaluation."),
    disable_tqdm: bool = typer.Option(False, help="Whether to disable the progress bar."),
    dataloader_num_workers: int = typer.Option(8, help="Number of subprocesses to use for data loading."),
    seed: int = typer.Option(42, help="Random seed."),
    num_classes: int = typer.Option(6, help="Number of classes for classification.")  # Add num_classes option
):
    model = torch.load(model_path)
    test_data = pd.read_csv(test_data_path)

    results = evaluate_model(
        model=model,
        test_data=test_data,
        model_type=model_type,
        output_dir=output_dir,
        logging_dir=logging_dir,
        eval_batch_size=eval_batch_size,
        disable_tqdm=disable_tqdm,
        dataloader_num_workers=dataloader_num_workers,
        seed=seed,
        num_classes=num_classes  # Pass num_classes parameter
    )

    print(results)

if __name__ == "__main__":
    app()
