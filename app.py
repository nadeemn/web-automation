import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def save_results(question, response):
    with open('results.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([question, response])

def navigate_questions(driver):
    try:
        question_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "glide__slide--active .theses__text")))
        print(question_element.text)

        action_buttons = driver.find_element(By.CLASS_NAME, "glide__slide--active .theses__box__footer .theses__actions")
        response_options = action_buttons.find_elements(By.TAG_NAME, 'li')

        for i, response in enumerate(response_options, start=1):
            response_text = response.find_element(By.TAG_NAME, 'span')
            print(i, response_text.text)

        input_response = int(input("enter the option number: ")) - 1

        if 0 <= input_response <= len(response_options):
            response_button = response_options[input_response].find_element(By.TAG_NAME, 'button')
            response_answer = response_options[input_response].find_element(By.TAG_NAME, 'span')
            
            save_results(question_element.text, response_answer.text)
            response_button.click()

        navigate_questions(driver)

    except (TimeoutException, NoSuchElementException):
        print("No more questions. Exiting")

    
def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html")

    button = driver.find_element(By.CLASS_NAME, "button--big")
    button.click()
    
    navigate_questions(driver)
    print("executed and file saved. Exiting")

if __name__ == "__main__":
    main()