class QAEmbedder:
  def __init__(self, model_name="paraphrase-MiniLM-L6-v2"):
    """
    Defines a QA embedding model. This is, given a set of questions,
    this class returns the corresponding embedding vectors.
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    self.model = None
    self.tokenizer = None
    self.model_name = model_name
    self.set_model(model_name)
  
  
  def get_model(self, model_name):
    """
    Loads a general tokenizer and model using pytorch
    'AutoTokenizer' and 'AutoModel'
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer
  
  
  def set_model(self, model_name):
    """
    Sets a general tokenizer and model using the 'self.get_model'
    method.
    
    Args:
      model_name (`str`): Directory containing the necessary tokenizer
        and model files.
    """
    self.model, self.tokenizer = self.get_model(self.model_name)
  
  
  def _mean_pooling(self, model_output, attention_mask):
    """
    Internal method that takes a model output and an attention
    mask and outputs a mean pooling layer.
    
    Args:
      model_output (`torch.Tensor`): output from the QA model
      attention_mask (`torch.Tensor`): attention mask defined in the QA tokenizer
      
    Returns:
      The averaged tensor.
    """
    token_embeddings = model_output[0]
    
    input_mask_expanded = (
      attention_mask
      .unsqueeze(-1)
      .expand(token_embeddings.size())
      .float()
    )
    
    pool_emb = (
      torch.sum(token_embeddings * input_mask_expanded, 1) 
      / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    )
    
    return pool_emb
  
  
  def get_embeddings(self, questions, batch=32):
    """
    Gets the corresponding embeddings for a set of input 'questions'.
    
    Args:
      questions (`list` of `str`): List of strings defining the questions to be embedded
      batch (`int`): Performs the embedding job 'batch' questions at a time
      
    Returns:
      The embedding vectors.
    """
    question_embeddings = []
    for i in range(0, len(questions), batch):
    
        # Tokenize sentences
        encoded_input = self.tokenizer(questions[i:i+batch], padding=True, truncation=True, return_tensors='pt')

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)

        # Perform mean pooling
        batch_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])
        question_embeddings.append(batch_embeddings)
    
    question_embeddings = torch.cat(question_embeddings, dim=0)
    return question_embeddings