from playwright.sync_api import sync_playwright
from self_healer import self_heal, generate_golden_identifier, capture_element_attributes, load_global_golden_data, store_global_golden_data

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto('http://localhost:8000/form.html')
        CURRENT_URL = page.url

        def inject_js():
            js_code = '''
            () => {
                function getSelector(el) {
                    if (el.id) return '#' + el.id;
                    if (el.className) return el.tagName.toLowerCase() + '.' + el.className.split(' ').join('.');
                    return el.tagName.toLowerCase();
                }
                // Track clicks, inputs, and dropdown changes
                document.addEventListener('click', function(event) {
                    const selector = getSelector(event.target);
                    console.log(JSON.stringify({type: 'click', selector: selector, timestamp: Date.now()}));
                });
                document.addEventListener('input', function(event) {
                    const selector = getSelector(event.target);
                    console.log(JSON.stringify({type: 'input', selector: selector, value: event.target.value, timestamp: Date.now()}));
                });
                // Special handling for dropdowns
                document.querySelectorAll('select').forEach(select => {
                    select.addEventListener('change', function(event) {
                        const selector = getSelector(event.target);
                        console.log(JSON.stringify({
                            type: 'dropdown',
                            selector: selector,
                            value: event.target.value,
                            timestamp: Date.now()
                        }));
                    });
                });
            }
            '''
            page.evaluate(js_code)

        inject_js()
        page.on('framenavigated', lambda _: inject_js())

        if page.query_selector('#employeeId'):
            page.click('#employeeId')
            elem = page.query_selector('#employeeId')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('employeeId', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#employeeId'):
            page.click('#employeeId')
            elem = page.query_selector('#employeeId')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('employeeId', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#employeeId'):
            page.fill('#employeeId', '1223')
            elem = page.query_selector('#employeeId')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('employeeId', page)
            page.fill(healed_selector, '1223')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#firstName'):
            page.click('#firstName')
            elem = page.query_selector('#firstName')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('firstName', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#firstName'):
            page.fill('#firstName', 'asasd')
            elem = page.query_selector('#firstName')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('firstName', page)
            page.fill(healed_selector, 'asasd')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#lastName'):
            page.click('#lastName')
            elem = page.query_selector('#lastName')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('lastName', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#lastName'):
            page.fill('#lastName', 'adsd')
            elem = page.query_selector('#lastName')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('lastName', page)
            page.fill(healed_selector, 'adsd')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#email'):
            page.click('#email')
            elem = page.query_selector('#email')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('email', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#email'):
            page.fill('#email', 'asddasd@add')
            elem = page.query_selector('#email')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('email', page)
            page.fill(healed_selector, 'asddasd@add')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#gender'):
            page.click('#gender')
            elem = page.query_selector('#gender')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('gender', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#gender'):
            page.fill('#gender', 'male')
            elem = page.query_selector('#gender')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('gender', page)
            page.fill(healed_selector, 'male')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        # Handling dropdown selection
        if page.query_selector('#gender'):
            page.select_option('#gender', value='male')
            elem = page.query_selector('#gender')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('gender', page)
            page.select_option(healed_selector, value='male')
        page.wait_for_timeout(1000)  # Shorter wait for dropdowns
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#gender'):
            page.click('#gender')
            elem = page.query_selector('#gender')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('gender', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#bloodGroup'):
            page.click('#bloodGroup')
            elem = page.query_selector('#bloodGroup')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('bloodGroup', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#bloodGroup'):
            page.fill('#bloodGroup', 'O+')
            elem = page.query_selector('#bloodGroup')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('bloodGroup', page)
            page.fill(healed_selector, 'O+')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        # Handling dropdown selection
        if page.query_selector('#bloodGroup'):
            page.select_option('#bloodGroup', value='O+')
            elem = page.query_selector('#bloodGroup')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('bloodGroup', page)
            page.select_option(healed_selector, value='O+')
        page.wait_for_timeout(1000)  # Shorter wait for dropdowns
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#bloodGroup'):
            page.click('#bloodGroup')
            elem = page.query_selector('#bloodGroup')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('bloodGroup', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#address'):
            page.click('#address')
            elem = page.query_selector('#address')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('address', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('#address'):
            page.fill('#address', 'sdsfsdfsas')
            elem = page.query_selector('#address')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('address', page)
            page.fill(healed_selector, 'sdsfsdfsas')
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        if page.query_selector('button'):
            page.click('button')
            elem = page.query_selector('button')
            golden_key = generate_golden_identifier(page, '{selector}', elem)
            golden_data = load_global_golden_data()
            golden_data[golden_key] = capture_element_attributes(elem)
            store_global_golden_data(golden_data)
        else:
            healed_selector = self_heal('utton', page)
            page.click(healed_selector)
        page.wait_for_timeout(2000)  # Wait 2 seconds
        new_url = page.url
        if new_url != CURRENT_URL:
            CURRENT_URL = new_url
            print('Navigation detected. New URL:', CURRENT_URL)
        browser.close()

if __name__ == '__main__':
    run_test()
