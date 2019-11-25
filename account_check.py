#!/usr/bin/python3.7

from selenium import webdriver as wd
import csv
import sys

def init_wd():
    chrome_options = wd.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = wd.Chrome(options=chrome_options)
    driver.implicitly_wait(10)

    return driver

def check_args():
    if (len(sys.argv) != 3):
        print("Usage:\n")
        print("python {} [CSV-input-file] [CSV-output-file]")
        sys.exit()

def parse_csv():
    clients = []
    with open(sys.argv[1], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            clients.append(row['Account Name'])

    return clients

def write_csv(workday_accounts):
    with open(sys.argv[2], mode='w') as csv_output_file:
        writer = csv.writer(csv_output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Account Name', 'Is In Workday'])
        for account in workday_accounts:
            writer.writerow([account[0], account[1]])

def is_in_workday(driver, search_button, account):
    search_button.send_keys(account)
    keep_loading = True
    while (keep_loading == True):
        lm = driver.find_element_by_tag_name('button')
        if (lm.text == 'Load more'):
            try:
                lm.click()
            except:
                break
        else:
            keep_loading = False
    
    attempts = 0
    found = False
    while (attempts < 10): 
        attempts += 1
        try:
            results = driver.find_elements_by_xpath('//wd-toggle/div[@class="toggle"][1]')
            for result in results:
                content = result.get_attribute('innerHTML')
                if account.lower() in content.lower():
                    found = True
                
            break
    
        except:
            continue

    search_button.clear()
    return found


if __name__ == "__main__":
    check_args()
    account_list = parse_csv()
    workday_accounts = []

    driver = init_wd()
    driver.get("https://www.workday.com/en-us/customers.html#?q=")
    search_button = driver.find_element_by_id("q")

    for account in account_list:
        if is_in_workday(driver, search_button, account):
            workday_accounts.append((account, 'yes'))
        else:
            workday_accounts.append((account, 'no'))

    write_csv(workday_accounts)

    driver.quit()
