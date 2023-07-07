import subprocess
import time
import streamlit as st
import os
import json
from PIL import Image

scripts = [
    './data_gen_load/content_gen.py',
    './data_gen_load/img_gen.py',
    #'./data_gen_load/cloudinary_upload.py',
    #'./data_gen_load/pre_fb_cleanup.py',
    #'./data_gen_load/translator_cost_effective.py',
    #'./data_gen_load/firebase_upload.py',
]
scripts_1 = [
    #'./data_gen_load/content_gen.py',
    #'./data_gen_load/img_gen.py',
    './data_gen_load/cloudinary_upload.py',
    './data_gen_load/pre_fb_cleanup.py',
    './data_gen_load/translator_cost_effective.py',
    './data_gen_load/firebase_upload.py',
]

st.title('Article generator')

topic = st.text_input('Type the topic/title for Article to be generated:')
submit_button = st.button('Submit')

# Determine present working directory
present_dir = os.getcwd()
filepath = os.path.join(present_dir, 'inputs.json')

if submit_button and topic != '':
    input_data = {topic: {'topic': topic, 'article_num': 1}}
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(input_data, f, ensure_ascii=False, indent=4)

    max_retries = 3
    retry_delay = 5
    processes = []

    for script in scripts:
        retry_count = 0
        while retry_count < max_retries:
            try:
                st.write(f'{script} is running ...')
                process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                processes.append(process)
                output, error = process.communicate()
                st.write(f"--- Output from {script} ---")
                st.code(output)

                # Display error only if there is an error message
                if error:
                    st.write(f"--- Error from {script} ---")
                    st.code(error)
                st.write(f'{script} has finished running.')

                # Check if there is any unexpected null output or error
                if output is None or error is None:
                    st.error(f"Unexpected null output or error from script '{script}'. Stopping the execution.")
                    break

                break
            except Exception as e:
                retry_count += 1
                st.error(f"Error running script '{script}': {str(e)}")
                st.info(f"Retrying {script} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            st.error(f"Max retries exceeded for script '{script}'. Skipping...")
            break

        # Rest of the code for processing each script
        if script == './data_gen_load/content_gen.py':
            process.wait()  # make sure the process is done
            directory_path = './outputs/content/'
            files = os.listdir(directory_path)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
            latest_content_json = os.path.join(directory_path, latest_file)
            with open(latest_content_json) as f:
                data = json.load(f)
            for topic, article in data.items():
                st.write('---')
                #st.subheader(f"Topic: {topic}")
                st.write(f"Category: {article['category']}")
                st.subheader(f"Title: {article['title']}")
                st.write(f"Content: {article['content']}")

        if script == './data_gen_load/img_gen.py':
            process.wait()  # make sure the process is done
            with open('outputs/json_with_img_path/article_data_imageUrl_slug.json') as f:
                data = json.load(f)
            for topic, article in data.items():
                img_path = article['Image_url']
                image = Image.open(img_path)
                st.image(image, caption=f'generated_image_{article["Slug"]}', use_column_width=True)

genre = st.radio(
        "Have you reviewed the article?",
        ('Publish', 'Abort')
        )

if genre == 'Publish':
        button_label = ":green[Publish]"
else:
    button_label = ":red[Abort]"

publish_button = st.button(button_label)



if publish_button and genre != '':
    
                st.write("As you say!")
                
                if genre == 'Publish':
                    st.write('Publishing Article')
                else:
                    st.write("Resetting. Try another idea")
                    # Delete the input.json file
                    inputs_filepath = os.path.join(present_dir, 'inputdummy.json')
                    if os.path.exists(inputs_filepath):
                        os.remove(inputs_filepath)
                    st.error("Execution aborted.")
                    st.experimental_rerun()
            


                

        if script == './data_gen_load/firebase_upload.py':
            process.wait()  # make sure the process is done
            st.write('Content uploaded successfully!')
            # Delete the input.json file
            inputs_filepath = os.path.join(present_dir, 'inputs.json')
            if os.path.exists(inputs_filepath):
                os.remove(inputs_filepath)
            st.experimental_rerun()

    for script in scripts_1:
        retry_count = 0
        while retry_count < max_retries:
            try:
                st.write(f'{script} is running ...')
                process = subprocess.Popen(['python', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                processes.append(process)
                output, error = process.communicate()
                st.write(f"--- Output from {script} ---")
                st.code(output)

                # Display error only if there is an error message
                if error:
                    st.write(f"--- Error from {script} ---")
                    st.code(error)
                st.write(f'{script} has finished running.')

                # Check if there is any unexpected null output or error
                if output is None or error is None:
                    st.error(f"Unexpected null output or error from script '{script}'. Stopping the execution.")
                    break

                break
            except Exception as e:
                retry_count += 1
                st.error(f"Error running script '{script}': {str(e)}")
                st.info(f"Retrying {script} in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            st.error(f"Max retries exceeded for script '{script}'. Skipping...")
            break

        # Rest of the code for processing each script
        if script == './data_gen_load/content_gen.py':
            process.wait()  # make sure the process is done
            directory_path = './outputs/content/'
            files = os.listdir(directory_path)
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
            latest_content_json = os.path.join(directory_path, latest_file)
            with open(latest_content_json) as f:
                data = json.load(f)
            for topic, article in data.items():
                st.write('---')
                #st.subheader(f"Topic: {topic}")
                st.write(f"Category: {article['category']}")
                st.subheader(f"Title: {article['title']}")
                st.write(f"Content: {article['content']}")

        if script == './data_gen_load/img_gen.py':
            process.wait()  # make sure the process is done
            with open('outputs/json_with_img_path/article_data_imageUrl_slug.json') as f:
                data = json.load(f)
            for topic, article in data.items():
                img_path = article['Image_url']
                image = Image.open(img_path)
                st.image(image, caption=f'generated_image_{article["Slug"]}', use_column_width=True)


            genre = st.radio(
                "Have you reviewed the article?",
                ('Publish', 'Abort')
            )

            if genre == 'Publish':
                button_label = ":green[Publish]"
            else:
                button_label = ":red[Abort]"

            button_clicked = st.button(button_label, key=f"button_{topic}")
            if button_clicked:
                st.session_state.clicked = True

            if st.session_state.clicked:
                st.write("As you say!")
                
                if genre == 'Publish':
                    st.write('Publishing Article')
                else:
                    st.write("Resetting. Try another idea")
                    # Delete the input.json file
                    inputs_filepath = os.path.join(present_dir, 'inputdummy.json')
                    if os.path.exists(inputs_filepath):
                        os.remove(inputs_filepath)
                    st.error("Execution aborted.")
                    st.experimental_rerun()


                

        if script == './data_gen_load/firebase_upload.py':
            process.wait()  # make sure the process is done
            st.write('Content uploaded successfully!')
            # Delete the input.json file
            inputs_filepath = os.path.join(present_dir, 'inputs.json')
            if os.path.exists(inputs_filepath):
                os.remove(inputs_filepath)
            st.experimental_rerun()