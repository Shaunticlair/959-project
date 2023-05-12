import csv

def process_txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as txt_file, open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['experiment', 'item', 'condition', 'sentence', 'prompt', 'question_type', 'options', 'literal_response', 'config'])
        
        experiment, item, condition, sentence = '', '', '', ''
        for line in txt_file:
            if line.startswith("#"):
                # Extract experiment, item, and condition
                experiment, item, condition, *_ = line[1:].strip().split()
                print(experiment, item, condition)
            elif line.startswith("?"):
                # Extract prompt
                parts = line.strip().split()
                literal_response = parts[-1]
                prompt= ' '.join(parts[1:-1])
                csv_writer.writerow([experiment, item, condition, sentence, prompt, 'multiple_choice', 'Yes_No', literal_response, ''])
            else:
                # Extract sentence and write row
                sentence = line.strip()

                

# Replace 'input.txt' and 'output.csv' with your desired input and output file names
#process_txt_to_csv('input.txt', 'output.csv')

import csv

def apply_html_formatting(input_csv, output_csv):
    with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Define the HTML formatting you want to apply
        def apply_font_formatting(text, font_family="'Comic Sans MS', cursive", font_size='16px', color='black'):
            return f'<span style="font-family: {font_family}; font-size: {font_size}; color: {color};">{text}</span>'

        header = next(csv_reader)
        csv_writer.writerow(header)

        # Find indices of 'sentence' and 'prompt' columns
        sentence_index = header.index('sentence')
        prompt_index = header.index('prompt')

        # Apply HTML formatting to the 'sentence' and 'prompt' columns and write to the output file
        for row in csv_reader:
            row[sentence_index] = apply_font_formatting(row[sentence_index])
            row[prompt_index] = apply_font_formatting(row[prompt_index])
            csv_writer.writerow(row)

# Replace 'input.csv' and 'output.csv' with your desired input and output file names
#apply_html_formatting('output.csv', 'new.csv')

from PIL import Image, ImageDraw, ImageFont

#Directory: go to home

def text_to_image(
    text: str,
    font_filepath: str,
    font_size: int,
    color: tuple[int, int, int, int]):

    font = ImageFont.truetype(font_filepath, size=font_size)

    img = Image.new("RGBA", (font.getmask(text).size[0]+20, font.getmask(text).size[1]+20 ) )

    draw = ImageDraw.Draw(img)
    draw_point = (0, -10)

    draw.multiline_text(draw_point, text, font=font, fill=color)

    text_window = img.getbbox()
    
    new_text_window = (text_window[0]-5, text_window[1]-5, text_window[2]+5, text_window[3]+5)
    img = img.crop(new_text_window)


    return img

#img = text_to_image('Hello World', 'comic.ttf', 72, (0, 0, 0, 255))

#Save image
options = '<img src="https://github.com/Shaunticlair/959-project/blob/main/comicyes.png?raw=true" width="25” height ="25">_<img src="https://github.com/Shaunticlair/959-project/blob/main/comicno.png?raw=true" width="20” height ="30">'
#img.save('text.png')
#Create helper functions for formatting
html_file = lambda name, width: f'<img src="https://github.com/Shaunticlair/959-project/blob/main/font_stuff/{name}?raw=true" width="{width}” height ="300">'
html_file = lambda name, width: f'<img src="https://sruiz-files.s3.us-east-2.amazonaws.com/{name}?raw=true" width="{width}” height ="300">'

font_file = lambda name: f'{name}.ttf'

def csv_gen_font_images(font, input_csv, output_csv):

    with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:

        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        #Iterate through each row in the csv
        for row in csv_reader:
            #Skip the header row
            if row[0] == 'experiment':
                csv_writer.writerow(row)
                continue
            #Get the sentence and prompt from the row
            sentence = row[3]
            prompt = row[4]

            sentence_width = round(300* (len(sentence))/40)
            prompt_width = round(300* (len(prompt))/40)


            #Create an image for the sentence and prompt
            sentence_img = text_to_image(sentence, font_file(font), 72, (0, 0, 0, 255))
            prompt_img = text_to_image(prompt, font_file(font), 72, (0, 0, 0, 255))

            sentence_image_name = f'{font}_{sentence}.png'.replace('?','').replace('/','')
            prompt_image_name = f'{font}_{prompt}.png'.replace('?','').replace('/','')

            #Save the image
            sentence_img.save(sentence_image_name)
            prompt_img.save(prompt_image_name)

            #Replace the sentence and prompt with the html code
            row[3] = html_file(sentence_image_name,sentence_width) #Sentence
            row[4] = html_file(prompt_image_name, prompt_width) #Prompt
            row[6] = options #Options

            #Write the row to the output file
            csv_writer.writerow(row)

#Create an image that says yes or no
def csv_gen_yes_no_images(font):
    yes_img = text_to_image('Yes', font_file(font), 72, (0, 0, 0, 255))
    no_img = text_to_image('No', font_file(font), 72, (0, 0, 0, 255))

    yes_img.save(f'{font}_yes.png')
    no_img.save(f'{font}_no.png')

#csv_gen_yes_no_images('comic')

#csv_gen_font_images('comic', 'font_stuff/base_stimuli.csv', 'comic stimuli.csv')


def link_to_yesno(input_csv, output_csv):
    yeslink = '<img src="https://github.com/Shaunticlair/959-project/blob/main/comicyes.png?raw=true" width="25” height ="25">'
    nolink = '<img src="https://github.com/Shaunticlair/959-project/blob/main/comicno.png?raw=true" width="20” height ="30">'

    with open(input_csv, 'r') as input_file, open(output_csv, 'w', newline='') as output_file:
        #Grab row 6, response

        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        for row in csv_reader:
            if row[0] == 'participant_id':
                csv_writer.writerow(row)
                continue
            print(row[6])
            if row[6] == yeslink:
                row[6] = 'Yes'
            elif row[6] == nolink:
                row[6] = 'No'
            csv_writer.writerow(row)

link_to_yesno('9.59 Extension.csv', '9.59_Extension_5_participants.csv')

