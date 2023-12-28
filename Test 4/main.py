import streamlit as st
from transformers import BartTokenizer, BartForConditionalGeneration

# Streamlit app
def main():
    st.title("Text Summarizer")

    # User input
    user_input = st.text_area("Enter text to summarize:", height=200)

    # Check if the user has entered text
    if st.button("Summarize"):
        if user_input:
            # Generate summary
            summary = generate_summary(user_input)
            # Display the summary
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter text to summarize.")

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

# Function to generate summary
def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

if __name__ == "__main__":
    main()
