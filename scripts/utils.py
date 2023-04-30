import json
import openai

class Utils:
       
    def createChunks(self, max_chunk_length, text):
        # ************************************************************
        # Generate chunks      
        # ************************************************************
        # Define the maximum length for each chunk
        # Split the text into smaller chunks
        self.max_chunk_length = max_chunk_length
        self.text = text
        chunks = []
        current_chunk = ""
        for sentence in self.text.split(". "):
            if len(current_chunk) + len(sentence) < self.max_chunk_length:
                current_chunk += sentence + ". "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        # Append the last chunk
        chunks.append(current_chunk.strip())
        return chunks

    def getAPIKeys(self):
        self.OPENAI_API_KEY = ""
        # ************************************************************
        # Read the token       
        # ************************************************************
        with open('config.json', 'r') as file_to_read:
            json_data = json.load(file_to_read)
            self.OPENAI_API_KEY = json_data["OPENAI_API_KEY"]
            openai.api_key =  self.OPENAI_API_KEY
            return openai

