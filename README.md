# AutoGrader
The above project is used to evaluate handwritten exam answer scripts. We have fine tuned Llama2 for this task and also created a RAG pipeline to display the page of the textbook where the answer to that question is present. Finally, we have deployed this model on AWS SageMaker and created a Lambda function to handle requests from the REST API. This project is fine tuned to evaluate answer scripts for the course Operating Systems only and every question is graded from 1-5. 

# Step 1: Dataset Generation

Dataset is generated by collecting questions from the course Operating Systems and the answers to each of the questions given by students and the corresponding score 1-5 is collected from the teacher. The dataset contains of around 116 entries and has 7 coloumns in which contain: 
1. Question
2. Answer given by the student
3. Grade given by the techer for the corresponding answer
4. Temp - It is the input format for the LLM model excluding Llama2
5. Text - It is the input format for fine tuning the LLM model Llama2
6. context- This is created for the RAG pipeline
7. text - This is the updated input format for fine tuning the LLM model Llama2 after introducing the RAG pipeline  

The dataset is found in the [Dataset.csv](https://github.com/PranavDarshan/AutoGrader/blob/main/Dataset.csv)

# Step 2: Finetuning Llama2 7B 

# Step 3: Creating a RAG Pipeline

# Step 4: Deploying Fine Tuned Model on AWS SageMaker

# Step 5: Handwriting to Text Conversion


# Step 5: Integrating with UI/UX

# Results
<p align=center>
<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/ModelResult.jpg width=700, height=300>
<img src=https://github.com/PranavDarshan/AutoGrader/blob/main/assets/RAG.jpg width=700, height=700>
</p>




