import concurrent.futures
import logging
import os
from typing import Any
from pydantic import BaseModel
from unstructured.partition.pdf import partition_pdf
import fitz

class OCR:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.logger = self.setup_logger()
    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        fh = logging.FileHandler('ocr_log.txt')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    #def process_partition(self, page_number):
    def process_partition(self):
        try:
            self.logger.info("STarting OCR")
            result = partition_pdf(
                filename=self.pdf_path,
                extract_images_in_pdf=False,
                infer_table_structure=True,
                chunking_strategy="by_title",
                max_characters=1000,
                new_after_n_chars=3800,
                combine_text_under_n_chars=2000,
                image_output_dir_path=".",
                #page_number=page_number,
            )
            self.logger.info("OCR Complete")
            #import pdb;pdb.set_trace()
            return result
        except Exception as e:
            self.logger.error(f"Error processing page : {e}")
            return []

    def get_num_pages(self):
        try:
            self.logger.info(f"Getting pages")
            doc = fitz.open(self.pdf_path)
            num_pages = doc.page_count
            self.logger.info("No of pages:"+str(num_pages))
            doc.close()
            return num_pages
        except Exception as e:
            self.logger.error(f"Error getting number of pages: {e}")
            return 0


    
    def process_pdf(self): 
        try:
            num_pages = self.get_num_pages()
            raw_pdf_elements = self.process_partition()
            
            return num_pages,raw_pdf_elements
        except Exception as e:
            self.logger.error(f"Error processing PDF: {e}")
            return []
