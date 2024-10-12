import fitz
import cv2
import numpy as np
import os

def process_and_crop_pdf_pages(pdf_path, crop_folder, zoom=2.0):
    pdf_document = fitz.open(pdf_path)
    page_counter = 0

    if not os.path.exists(crop_folder):
        os.makedirs(crop_folder)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)  
        zoom_matrix = fitz.Matrix(zoom, zoom)  # zoom due to blurry pictures
        pix = page.get_pixmap(matrix=zoom_matrix)  
        
        # colors were off idk why, but this fixed it
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        if pix.n == 4:  
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        elif pix.n == 3: 
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        crops = detect_and_crop_tables_from_image(img, crop_folder, page_number + 1)
        print(f"{crops} cropped regions saved from page {page_number + 1}.")
        page_counter += 1

    return page_counter

def detect_and_crop_tables_from_image(image, output_folder, page_number):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(blurred, 50, 200)

    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    bounding_boxes = []
    crop_counter = 0

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if w > 100 and h > 50:  # can change based on pdf size
            overlap = False
            for (prev_x, prev_y, prev_w, prev_h) in bounding_boxes:
                if (x < prev_x + prev_w and x + w > prev_x and y < prev_y + prev_h and y + h > prev_y):
                    overlap = True
                    break

            if not overlap:
                bounding_boxes.append((x, y, w, h)) 
                cropped_image = image[y:y+h, x:x+w] 
                crop_filename = f"page_{page_number}_{crop_counter}.png"
                crop_path = os.path.join(output_folder, crop_filename)
                cv2.imwrite(crop_path, cropped_image)  
                crop_counter += 1
                print(f"cropped saved as {crop_filename}")
    
    return crop_counter

def scrape_pdf_and_crop(pdf_path, crop_folder, zoom=2.0):
    pages_processed = process_and_crop_pdf_pages(pdf_path, crop_folder, zoom)
    print(f"{pages_processed} pages cropped, saved in {crop_folder}.")

pdf_path = "2013report.pdf"  # pdf file path
crop_folder = "2013cropped"  # path to save folder
scrape_pdf_and_crop(pdf_path, crop_folder)
