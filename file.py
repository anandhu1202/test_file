import json
from playwright.sync_api import sync_playwright
from self_healer import self_heal, generate_golden_identifier, capture_element_attributes, load_global_golden_data, store_global_golden_data

# List to store recorded events
recorded_events = []


def handle_console_message(msg):
    try:
        data = json.loads(msg.text)
        if "type" in data:
            recorded_events.append(data)
            print("Recorded event:", data)
    except Exception:
        pass

def deduplicate_events(events):
    """
    Remove redundant input events, keeping only the last input per selector.
    """
    filtered = []
    i = 0
    while i < len(events):
        event = events[i]
        if event.get("type") != "input":
            filtered.append(event)
            i += 1
        else:
            final_event = event
            j = i + 1
            while j < len(events) and events[j].get("type") == "input" and events[j].get("selector") == event.get("selector"):
                final_event = events[j]
                j += 1
            filtered.append(final_event)
            i = j
    return filtered

def generate_test_script(events, website):
    filtered_events = deduplicate_events(events)

    script_lines = [
        "from playwright.sync_api import sync_playwright",
        "from self_healer import self_heal, generate_golden_identifier, capture_element_attributes, load_global_golden_data, store_global_golden_data",
        "",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=False)",
        "        page = browser.new_page()",
        f"        page.goto('{website}')",
        "        CURRENT_URL = page.url",
        "",
        "        def inject_js():",
        "            js_code = '''",
        "            () => {",
        "                function getSelector(el) {",
        "                    if (el.id) return '#' + el.id;",
        "                    if (el.className) return el.tagName.toLowerCase() + '.' + el.className.split(' ').join('.');",
        "                    return el.tagName.toLowerCase();",
        "                }",
        "                // Track clicks, inputs, and dropdown changes",
        "                document.addEventListener('click', function(event) {",
        "                    const selector = getSelector(event.target);",
        "                    console.log(JSON.stringify({type: 'click', selector: selector, timestamp: Date.now()}));",
        "                });",
        "                document.addEventListener('input', function(event) {",
        "                    const selector = getSelector(event.target);",
        "                    console.log(JSON.stringify({type: 'input', selector: selector, value: event.target.value, timestamp: Date.now()}));",
        "                });",
        "                // Special handling for dropdowns",
        "                document.querySelectorAll('select').forEach(select => {",
        "                    select.addEventListener('change', function(event) {",
        "                        const selector = getSelector(event.target);",
        "                        console.log(JSON.stringify({",
        "                            type: 'dropdown',",
        "                            selector: selector,",
        "                            value: event.target.value,",
        "                            timestamp: Date.now()",
        "                        }));",
        "                    });",
        "                });",
        "            }",
        "            '''",
        "            page.evaluate(js_code)",
        "",
        "        inject_js()",
        "        page.on('framenavigated', lambda _: inject_js())",
        ""
    ]

    for event in filtered_events:
        selector = event.get("selector", "")
        if not selector:
            continue

        if event.get("type") == "click":
            script_lines.extend([
                f"        if page.query_selector('{selector}'):",
                f"            page.click('{selector}')",
                f"            elem = page.query_selector('{selector}')",
                "            golden_key = generate_golden_identifier(page, '{selector}', elem)",
                "            golden_data = load_global_golden_data()",
                "            golden_data[golden_key] = capture_element_attributes(elem)",
                "            store_global_golden_data(golden_data)",
                "        else:",
                f"            healed_selector = self_heal('{selector[1:]}', page)",
                "            page.click(healed_selector)",
                "        page.wait_for_timeout(2000)  # Wait 2 seconds",
                "        new_url = page.url",
                "        if new_url != CURRENT_URL:",
                "            CURRENT_URL = new_url",
                "            print('Navigation detected. New URL:', CURRENT_URL)",
            ])

        elif event.get("type") == "input":
            value = event.get("value", "")
            script_lines.extend([
                f"        if page.query_selector('{selector}'):",
                f"            page.fill('{selector}', '{value}')",
                f"            elem = page.query_selector('{selector}')",
                "            golden_key = generate_golden_identifier(page, '{selector}', elem)",
                "            golden_data = load_global_golden_data()",
                "            golden_data[golden_key] = capture_element_attributes(elem)",
                "            store_global_golden_data(golden_data)",
                "        else:",
                f"            healed_selector = self_heal('{selector[1:]}', page)",
                f"            page.fill(healed_selector, '{value}')",
                "        new_url = page.url",
                "        if new_url != CURRENT_URL:",
                "            CURRENT_URL = new_url",
                "            print('Navigation detected. New URL:', CURRENT_URL)",
            ])

        elif event.get("type") == "dropdown":
            value = event.get("value", "")
            script_lines.extend([
                f"        # Handling dropdown selection",
                f"        if page.query_selector('{selector}'):",
                f"            page.select_option('{selector}', value='{value}')",
                f"            elem = page.query_selector('{selector}')",
                "            golden_key = generate_golden_identifier(page, '{selector}', elem)",
                "            golden_data = load_global_golden_data()",
                "            golden_data[golden_key] = capture_element_attributes(elem)",
                "            store_global_golden_data(golden_data)",
                "        else:",
                f"            healed_selector = self_heal('{selector[1:]}', page)",
                f"            page.select_option(healed_selector, value='{value}')",
                "        page.wait_for_timeout(1000)  # Shorter wait for dropdowns",
                "        new_url = page.url",
                "        if new_url != CURRENT_URL:",
                "            CURRENT_URL = new_url",
                "            print('Navigation detected. New URL:', CURRENT_URL)",
            ])

    script_lines.append("        browser.close()")
    script_lines.append("")
    script_lines.append("if __name__ == '__main__':")
    script_lines.append("    run_test()")

    return "\n".join(script_lines)


def main():
    website = input("Enter website URL (include http:// or https://): ").strip()
    if not website:
        print("No website provided. Exiting.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(website)

        def inject_js(page):
            js_code = """
            () => {
                function getSelector(el) {
                    if (el.id) return '#' + el.id;
                    if (el.className) return el.tagName.toLowerCase() + '.' + el.className.split(' ').join('.');
                    return el.tagName.toLowerCase();
                }

                // Existing event listeners
                document.addEventListener('click', function(event) {
                    const selector = getSelector(event.target);
                    console.log(JSON.stringify({type: 'click', selector: selector, timestamp: Date.now()}));
                });

                document.addEventListener('input', function(event) {
                    const selector = getSelector(event.target);
                    console.log(JSON.stringify({type: 'input', selector: selector, value: event.target.value, timestamp: Date.now()}));
                });

                // New dropdown handling
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
            """
            try:
                page.evaluate(js_code)
            except Exception as e:
                print(f"Error injecting JavaScript: {str(e)}")

        inject_js(page)
        page.on("framenavigated", lambda _: inject_js(page))
        page.on("console", handle_console_message)

        print(f"Browser launched and recording events on {website}.")
        print("Interact with the page. When finished, press Enter in this terminal to stop recording...")
        input()

        print("Stopping recording and closing browser...")
        browser.close()

    print("\nRecorded events:")
    for event in recorded_events:
        print(event)

    test_script = generate_test_script(recorded_events, website)
    with open("generated_test.py", "w") as f:
        f.write(test_script)

    print("\nTest script generated and saved as 'generated_test.py'.")
    print("Run it with: python generated_test.py")

if __name__ == "__main__":
    main()
