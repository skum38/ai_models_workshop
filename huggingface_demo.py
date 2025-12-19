from transformers import pipeline
def main():
    # Initialize a text generation pipeline using a pre-trained model
    text_generator = pipeline("text-generation", model="gpt2")

    # Generate text based on a prompt
    prompt = "Once upon a time in a land far, far away"
    generated_text = text_generator(prompt, max_length=50, num_return_sequences=1)

    # Print the generated text
    print(generated_text[0]['generated_text']) 

if __name__ == "__main__":
    main()
