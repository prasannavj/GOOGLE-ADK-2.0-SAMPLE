from google.adk.events import Event
from google.adk import Workflow # type: ignore
from google.adk import Agent
from pydantic import BaseModel
'''
Twitter Post Generator
1. User enters a Topic, thus triggering Workflow execution
2. This Topic is supplied to top_keyword_finder_agent as String
3. The output of this node is KeywordTopicModel containing keyword, supplied as input to next node twitter_agent
4. The output of twitter_agent node is TwitterPostModel containing {topic,keyword,post}. Finally we may use `post` as output
'''
class KeywordTopicModel(BaseModel):
    keyword: str
    topic:str 
class TwitterPostModel(BaseModel):
    topic: str
    keyword: str
    post: str

top_keyword_finder_agent = Agent(
    name="top_keyword_finder_agent",
    model="gemini-flash-lite-latest",
    output_schema=KeywordTopicModel,
    instruction="""Find single topmost ranking keyword for topic supplied by user."""
)
twitter_agent = Agent(
    name="twitter_agent",
    model="gemini-flash-lite-latest",
    input_schema=KeywordTopicModel,
    output_schema=TwitterPostModel,
    instruction="""Write a twitter post for {KeywordTopicModel.keyword}.""",
)
root_agent = Workflow(
    name="root_agent",
    edges=[("START", top_keyword_finder_agent, twitter_agent)],
)
'''
top_keyword_finder_agent
    input: Google Antigravity 
    output: {keyword:'google anti gravity'}
twitter_agent   
    input: {keyword:'google anti gravity'}
    output: {topic:'Google Antigravity',keyword:'google anti gravity',
    post:'Want to break physics? Go search 'Google Anti Gravity' and hit 'I'm Feeling Lucky' to watch the homepage crash and float around! 🚀🪐 #GoogleTricks '} 
'''
