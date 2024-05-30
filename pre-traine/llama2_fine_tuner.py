from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import load_dataset
from transformers import DataCollatorForLanguageModeling

class LLaMA2FineTuner:
    def __init__(self, model_name, train_file, test_file, output_dir='./results', num_labels=2, max_length=512):
        self.model_name = model_name
        self.train_file = train_file
        self.test_file = test_file
        self.output_dir = output_dir
        self.num_labels = num_labels
        self.max_length = max_length

        try:
            # Load pre-trained model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
        except Exception as e:
            print(f"Error loading model or tokenizer: {e}")

    def load_and_tokenize_data(self):
        try:
            # Load and prepare the dataset
            self.dataset = load_dataset('csv', data_files={'train': self.train_file, 'test': self.test_file})

            # Tokenize the dataset
            def tokenize_function(examples):
                return self.tokenizer(examples['text'], padding="max_length", truncation=True, max_length=self.max_length)

            self.tokenized_datasets = self.dataset.map(tokenize_function, batched=True)
        except Exception as e:
            print(f"Error loading or tokenizing dataset: {e}")

    def setup_trainer(self, learning_rate=5e-5, per_device_train_batch_size=2, per_device_eval_batch_size=2, num_train_epochs=3, weight_decay=0.01, save_total_limit=1, save_steps=500):
        try:
            # Prepare DataLoader
            self.data_collator = DataCollatorForLanguageModeling(tokenizer=self.tokenizer, mlm=False)
            self.train_dataset = self.tokenized_datasets["train"]
            self.test_dataset = self.tokenized_datasets["test"]

            # Define training arguments
            self.training_args = TrainingArguments(
                output_dir=self.output_dir,
                evaluation_strategy="epoch",
                learning_rate=learning_rate,
                per_device_train_batch_size=per_device_train_batch_size,
                per_device_eval_batch_size=per_device_eval_batch_size,
                num_train_epochs=num_train_epochs,
                weight_decay=weight_decay,
                save_total_limit=save_total_limit,
                save_steps=save_steps,
            )

            # Create Trainer
            self.trainer = Trainer(
                model=self.model,
                args=self.training_args,
                train_dataset=self.train_dataset,
                eval_dataset=self.test_dataset,
                tokenizer=self.tokenizer,
                data_collator=self.data_collator,
            )
        except Exception as e:
            print(f"Error setting up trainer: {e}")

    def train(self):
        try:
            # Train the model
            self.trainer.train()
        except Exception as e:
            print(f"Error during training: {e}")

    def evaluate(self):
        try:
            # Evaluate the model
            metrics = self.trainer.evaluate()
            print(metrics)
            return metrics
        except Exception as e:
            print(f"Error during evaluation: {e}")

# Example usage
# if __name__ == "__main__":
#     model_name = 'meta-llama/Llama-2-7b'  # Example model name
#     train_file = 'train.csv'
#     test_file = 'test.csv'

#     fine_tuner = LLaMA2FineTuner(model_name, train_file, test_file)
#     fine_tuner.load_and_tokenize_data()
#     fine_tuner.setup_trainer()
#     fine_tuner.train()
#     metrics = fine_tuner.evaluate()
#     print("Training and evaluation completed.")
