# Robert-Ai: Empathic Emotional Support Robo Friend

## Overview

Robert-Ai is an application designed to provide empathetic emotional support. This bot combines cutting-edge technologies to deliver meaningful and helpful interactions for users seeking companionship and understanding. It is equipped with advanced AI models to ensure realistic and emotionally aware responses.

## Installation

### 1. Create a Directory and Move the Project

Ensure that your project is stored in a dedicated directory on your system:

```bash
mkdir "C:\Robert Ai-Assignment 3 Part 2\law_consultant_robert\constitution_app"
```

Move the project files into this directory.

### 2. Clone the Repository

```bash
git clone https://github.com/nova-fibeyli/Robert-Ai-Assignment-3-Part-2.git
cd Robert-Ai
```

### 3. Install the Required Dependencies

```bash
cd "C:\Robert Ai-Assignment 3 Part 2\law_consultant_robert\constitution_app"
pip install -r requirements.txt
```

### 4.Set API Key as an Environment Variable

Before running your script, set the key in the environment:

```
$env:OPENAI_API_KEY="your-openai-api-key"
```

You can get yours at: https://platform.openai.com/settings/proj_aFGBtPZL9XTDWQIQDGtBlgEP/api-keys
## Project Structure

The project follows a structured format to ensure organization and efficiency:

```
Main Application Code:
│── src/
│   ├── app.py (primary application file)
│   ├── other_module.py (potential auxiliary functionality)
│   ├── preprocess_and_load.py (data preprocessing)
│   ├── dataset/
│   │   ├── constitution.json (dataset used in the project)
│
Utilities:
│── src/utils/
│   ├── citation.py
│   ├── question_handler.py
|   ├── __pycache__/
|   |   ├──citation.cpython-312.pyc
|   |   ├──question_handler.cpython-312.pyc
│
Testing Files:
│── test/
│   ├── test_app.py
│   ├── test_preprocess.py
│   ├── app_test.py
│
Documentation and Requirements:
│── README.md
│── requirements.txt
│── LICENSE
```

## Key Features

### Core Functionalities

- **Multi-Query Retrieval**: Enables searching multiple queries efficiently.
- **Reciprocal Rank Fusion (RAG Fusion)**: Improves response ranking accuracy.
- **MongoDB Integration**: Stores and retrieves conversation history dynamically.
- **Streamlit Framework**: Provides an interactive and intuitive UI.
- **Ollama Integration**: Utilizes AI-powered language models for empathetic and human-like responses.
- **File Upload & Document Querying**:
  - Supports **.txt, .pdf, and .docx** file uploads.
  - Extracts and processes document content to provide relevant insights.
  - Allows users to ask questions based on uploaded content.
- **Datasets Used**:
  - **EmpathicDialogues**: Trained dataset for emotional intelligence in responses. From: https://github.com/facebookresearch/EmpatheticDialogues.git
  - **Constitution Dataset**: Provides legal document-based assistance.

## Usage

### 1. Start the Application

Run the following command to start the main application:

```bash
cd "C:\Robert Ai-Assignment 3 Part 2\law_consultant_robert\constitution_app\src"
streamlit run app.py
```

### 2. Upload Documents and Interact

- Enter messages or questions, and Robert-Ai will respond empathetically.
- Upload **.txt, .pdf, .docx** files to receive context-aware answers.
- Retrieve document-specific responses and engage with content interactively.

### 3. Alternative Precision Mode

For more precise responses, run:

```bash
streamlit run C:\law_consultant_robert\constitution_app\src\app_alt.py
```

## Technologies Used

- **Python**: The backbone of the application for scripting and development.
- **MongoDB**: NoSQL database to store conversation logs and facilitate dynamic responses.
- **Streamlit**: Interactive UI framework.
- **Ollama**: AI-based conversational capabilities.
- **PyMuPDF (fitz)**: Extracts text from uploaded PDF documents.
- **pymongo**: Enables MongoDB communication.

## MongoDB Access

You can log in to MongoDB with the following credentials:

- **Email**: `magzhan.ikram@astanait.edu.kz`
- **Password**: `<your-password>`
- **Login URL**: [MongoDB Login](https://account.mongodb.com/account/login?signedOut=true)
- ***

## Examples

**Example 1: Basic Conversation**

```
User: Hi Robert-Ai, I feel a bit down today.
Robert-Ai: I'm here for you. Do you want to talk about what's on your mind?
```

**Example 2: Document-Based Interaction**

```
User: Uploads "constitution.pdf"
User: What does Article 5 state?
Robert-Ai: Article 5 states that [relevant text extracted from the document].**Example 2: Document-Based Interaction**

**Example 3: Document-Based Interaction**

```

User: Uploads "Introduction to
Backend Web Development.pdf"
User: tell me what is here?

Robert-Ai: It seems like you have a document or presentation about Backend Web Development. Let me help break it down for you: **Overview** The document appears to be an introduction to backend web development, written by Rakhymbayeva Nazerke Imanbakhytovna. **Categories and Subcategories** The document is organized into several categories: 1. **Website**: Not much information here, just a reference to the website. 2. **Frontend**: References to frontend topics (3 mentions) 3. **Backend**: Introduces backend topics, including: _ Saves and manages data (4 mentions) _ Databases _ Microservice _ Data Service _ Email Service _ Queue (6 mentions) 4. **What Happens?**: A mysterious section that doesn't seem to be fully expanded. 5. **Computers can’t receive messages (by default)**: An interesting topic, but not much context here. 6. **Backend Programming Language**: Two references to backend programming languages (10 and 11), with a mention of "Backend Programming" later on. **Other Topics** The document also touches on: 1. Amazon Order 2. Client-Server architecture Let me know if you'd like me to help with anything specific or if there's anything else I can clarify!

```

## License

This project is licensed under the Apache License 2.0.

## Repository

Visit the project repository at [Robert-Ai GitHub Repository](https://github.com/nova-fibeyli/Robert-Ai-Assignment-3-Part-2.git).
```
