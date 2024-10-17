import os
import streamlit as st #important
from openai import OpenAI
from time import process_time_ns

client = OpenAI(
    api_key = os.environ['OpenAI_API_Key']
)


#Story
def story_gen(prompt):
  system_prompt = """
  You are a world renowned author for young adults fiction short stories.
  Given a concept, generate a short story relevant to the themes of the concept with a twist ending.
  The total length of the story not exceed 100 words and only english and character in utf-8.
  """

  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {'role':'system', 'content':system_prompt},
          {'role':'user', 'content':prompt}
      ],
      temperature = 1.6,
      max_tokens = 200
  )
  return response.choices[0].message.content


#Cover art
def art_gen(prompt):
  response = client.images.generate(
      model = 'dall-e-2',
      prompt = prompt,
      size = '256x256',
      n = 1
  )
  return response.data[0].url

#Cover prompt design
def design_gen(prompt):
  system_prompt = """
  You will be given a short story. Generate a prompt for a cover art that is suitable for the story.
  The prompt is for dall-e-2.
  """

  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {'role':'system', 'content':system_prompt},
          {'role':'user', 'content':prompt}
      ],
      temperature = 1.3,
      max_tokens = 200
  )
  return response.choices[0].message.content

#UI
prompt = st.text_input("Enter a prompt: ")
if st.button("Generate"):
    story = story_gen(prompt)
    design = design_gen(story)
    art = art_gen(design)

    st.caption(design)
    print('-'*50)
    st.write(story)
    print('-'*50)
    st.image(art)
