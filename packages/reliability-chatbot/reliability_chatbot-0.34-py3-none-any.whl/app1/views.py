from .models import User, ChatSession, SimilarQuestion, Feedback
import hashlib

from django.db import transaction


def generate_cluster_id(question):
    # Hash the question using SHA-256
    hash_object = hashlib.sha256(question.encode())
    
    # Get the hexadecimal representation of the hash
    hex_digest = hash_object.hexdigest()
    
    # Take the first 5 characters of the hexadecimal representation
    shortened_hex_digest = hex_digest[:5]
    
    # Combine the prefix with the shortened hexadecimal representation
    cluster_id = f"CL-ID_{shortened_hex_digest}"
    
    return cluster_id


from app1.decorators import api_key_required 


@api_key_required
def save_to_database(**kwargs):
    user_name = kwargs.get('user_name', 'DefaultUser')
    # session_id = kwargs.get('session_id', 'DefaultSessionID')
    question = kwargs.get('question', 'DefaultQuestion')
    answer = kwargs.get('answer', 'DefaultAnswer')

    cluster_id = generate_cluster_id(question)

    try:
        with transaction.atomic():
            # Assuming 'ChatSession' is the model and has been imported correctly.
            chat_session = ChatSession(
                user_name=user_name,
                # session_id=session_id,
                question=question,
                answer=answer,
                cluster_id=cluster_id
            )
            similar_session = SimilarQuestion(
                user_name=user_name,
                # session_id=session_id,
                question=question,
                answer=answer,
                cluster_id=cluster_id
            )
            chat_session.save()
            similar_session.save()
            print(f"Data saved for user {user_name}")
            return True
    except Exception as e:
        print(f"Failed to save data: {str(e)}")
        return False



from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import inflect
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@api_key_required
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    p = inflect.engine()

    def convert_number_to_words(token):
        if token.isdigit():
            return p.number_to_words(token)
        else:
            return token

    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(convert_number_to_words(token.lower())) for token in tokens]
    # print('lemmatized_tokens',lemmatized_tokens)
    return ' '.join(lemmatized_tokens)




def extract_number(question):
    # Extracting any number from the question
    match = re.search(r'\b(\d+)\b', question)
    return int(match.group(1)) if match else None



@api_key_required
def get_answer_from_database(question,user_name):
    print(question)
    try:
        # all_entries = ChatSession.objects.filter(user_name=user_name)
        all_entries = ChatSession.objects.filter(user_name__iexact=user_name)
        print(all_entries)

        
        if not all_entries:
            return None  # No questions in the database, return None
        
        current_question_session_number = extract_number(question)
        processed_current_question = preprocess_text(question)
        # print('processed_current_questions',processed_current_question)

        # Filter entries by session number if present
        relevant_entries = [entry for entry in all_entries if extract_number(entry.question) == current_question_session_number]
        # print('relevant_entries',relevant_entries)

        if not relevant_entries:
            return None  # No relevant entries found for the specific session

        processed_questions = [preprocess_text(entry.question) for entry in relevant_entries]
        processed_questions.append(processed_current_question)  # Adding the current question for similarity comparison
        # print('processed_questions',processed_questions)

        # Use SentenceTransformer for creating embeddings
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        question_embeddings = model.encode(processed_questions, convert_to_tensor=True)

        # Convert embeddings to NumPy arrays for similarity calculation
        question_embeddings_np = [embedding.cpu().detach().numpy() for embedding in question_embeddings]

        # Calculate cosine similarities
        similarities = cosine_similarity([question_embeddings_np[-1]], question_embeddings_np[:-1])
        # print('similarities',similarities)

        # Find the most similar question
        most_similar_index = similarities.argmax()
        most_similar_answer = relevant_entries[most_similar_index].answer
        print("All entries: ", all_entries.count())
        print("Processed current question: ", processed_current_question)
        print("Relevant entries count: ", len(relevant_entries))
        print("Similarities: ", similarities)

        
        similarity_threshold = 0.8 

        if similarities[0][most_similar_index] >= similarity_threshold:
            retrieved_entry = relevant_entries[most_similar_index]
            
            retrieved_entry.save() 
           
            # Create a SimilarQuestion object
            match = SimilarQuestion.objects.create(
                    question=question,
                    answer=retrieved_entry.answer,
                    cluster_id= retrieved_entry.cluster_id,
                    
                    user_name=user_name,
                    
                )

            return most_similar_answer
        else:
            return None

    except ChatSession.DoesNotExist:
        return None
    



from django.http import JsonResponse
import json
from django.http import HttpResponse

@api_key_required
def submit_feedback(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        question = request.POST.get('question')
        feedback_answer = request.POST.get('feedback_answer')
        feedback = request.POST.get('feedback')

        # Print the received data for debugging
        print(f"Received feedback -  Answer: {feedback_answer}, Type: {feedback}")

        # Convert feedback_type to boolean
        feedback_type_bool = True if feedback == 'positive' else False

        # Save the feedback to the database
        Feedback.objects.create(
            # username=username,
            question=question,
            answer=feedback_answer,
            feedback=feedback_type_bool
        )

        return HttpResponse("Thank you for your feedback!")
    else:
        return HttpResponse("Invalid request", status=400)