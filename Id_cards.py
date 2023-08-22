import barcode
from barcode import Code39
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont
import os

def main():

    # Function to filter OTPs based on first 7 digits of filenames
    def filter_otp(filename):
        otp = filename[:7]  # Extract first 7 characters from filename
        if otp.startswith("OPT-"):
            return otp[4:]  # Remove "OPT-" prefix
        else:
            return None


    # Get name and OPT number from user input
    name = input("Enter name: ")
    OPT = input("Enter OPT number: ")


    # Generate the barcode code
    code = "OPT-" + OPT


    # Generate and save the barcode image
    code39 = Code39(code, writer=ImageWriter(), add_checksum=False)
    generated_filename = code39.save('C:/Users/jhoang/Desktop/Id cards/Id cards/EmpBarcodes/' + code, {"module_width": 0.35, "module_height": 10, "font_size": 18, "text_distance": -2, "quiet_zone": 2, "write_text": False})
    print('Generated Code 39 barcode image file name: ' + generated_filename)


    # Create a blank sign-in card template
    card_width = 600
    card_height = 2000
    card_background_color = (255, 255, 255)
    outline_color = (0, 0, 0)  # Specify the outline color
    outline_thickness = 10  # Specify the outline thickness


    # Increase the card width and height to accommodate the outline
    card_width += 2 * outline_thickness
    card_height += 2 * outline_thickness


    card = Image.new('RGB', (card_width, card_height), card_background_color)
    draw = ImageDraw.Draw(card)  # Define the draw object


    # Add outline to the card
    outline_rect = [(0, 0), (card_width - 1, card_height - 1)]
    draw.rectangle(outline_rect, outline=outline_color, width=outline_thickness)


    # Load the Optima logo image
    logo_path = 'C:/Users/jhoang/Desktop/Id cards/Id cards/Optima.jpg'  # Replace with the actual path to your Optima logo image
    logo_width = 450
    logo_height = 115
    logo = Image.open(logo_path)
    logo = logo.resize((logo_width, logo_height))


    # Specify the folder name for employee photos
    folder_path = "C:/Users/jhoang/Desktop/Id cards/Id cards/EmpPhoto/"


    # Filter OTPs from filenames
    filenames = os.listdir(folder_path)
    filtered_filenames = [filename for filename in filenames if filter_otp(filename) == OPT]


    # Check if filtered_filenames list is empty
    if len(filtered_filenames) == 0:
        print(f"No employee photo found for OPT-{OPT}")
        exit()


    # Load the person's picture
    picture_path = os.path.join(folder_path, filtered_filenames[0])  # Use the first filtered filename
    picture_width = 375
    picture_height = 500
    picture = Image.open(picture_path)
    picture = picture.resize((picture_width, picture_height))


    # Add Optima logo to the card
    logo_position = (card_width // 2 - logo_width // 2, 20)
    card.paste(logo, logo_position)


    # Add the person's picture to the card
    picture_position = (card_width // 2 - picture_width // 2, logo_position[1] + logo_height + 20)
    card.paste(picture, picture_position)



    # Add the person's name to the card
    name_font_size = 40
    name_font = ImageFont.truetype("C:/Users/jhoang/Desktop/Id cards/Id cards/GT-Pressura-Extended-Medium.ttf", name_font_size)
    name_text = name
    name_text_position = (
        card_width // 2 - name_font.getsize(name_text)[0] // 2,
        picture_position[1] + picture_height + 20
    )
    draw.text(name_text_position, name_text, fill=(0, 0, 0), font=name_font)




    # Add the first barcode to the card
    barcode_image = Image.open("C:/Users/jhoang/Desktop/Id cards/Id cards/EmpBarcodes/" + code + ".png")  # Load the generated barcode image
    barcode_image_position = (
        card_width // 2 - barcode_image.width // 2,
        name_text_position[1] + name_font.getsize(name_text)[1] + 20
    )


    # Calculate the barcode image size with 10% margin
    barcode_width = int(barcode_image.width * 0.9)
    barcode_height = int(barcode_image.height * 0.9)




    # Resize the barcode image with 10% margin
    barcode_image = barcode_image.resize((barcode_width, barcode_height))




    # Calculate the barcode image positions with 10% margin
    barcode_image_position = (
        card_width // 2 - barcode_width // 2,
        name_text_position[1] + name_font.getsize(name_text)[1] + 20
    )


    card.paste(barcode_image, barcode_image_position)




    # Add the second barcode to the card
    barcode_image2 = barcode_image.rotate(90, expand=True)
    barcode_image2 = barcode_image2.resize((400, barcode_image2.height))
    barcode_image2_position = (
        card_width // 2 - barcode_image2.width // 2,
        barcode_image_position[1] + barcode_image.height + 300
    )
    card.paste(barcode_image2, barcode_image2_position)








    # Save and display the sign-in card
    card.save('C:/Users/jhoang/Desktop/Id cards/Id cards/EmpId/sign_in '+OPT+'.png')
    card.show()

if __name__ == "__main__":
    repeat = True
    while repeat:
        main()
        
main()



