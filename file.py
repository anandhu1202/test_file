import json
from playwright.sync_api import sync_playwright
from self_healer import self_heal, generate_golden_identifier, capture_element_attributes, load_global_golden_data, store_global_golden_data

# List to store recorded events
recorded_events = []

def handle_console_message(msg):
    """
    Parse JSON messages from the page's console.
    If the message contains a 'type' key, record it.
    """
    try:
        data = json.loads(msg.text)
        if "type" in data:
            recorded_events.append(data)
            print("Recorded event:", data)
    except Exception:
        # Ignore messages that aren't JSON-formatted
        pass

def deduplicate_events(events):
    """
    Filter out redundant input events.
    For a series of consecutive input events on the same selector,
    only the last event is kept.
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
    """
    Generate a Playwright test script that:
      - Navigates to the given website.
      - Replays recorded events (clicks and final input values),
        each wrapped in try/except blocks.
      - On a successful interaction, it captures the element's attributes
        and updates the golden file.
      - If an action fails, it uses self_heal to generate a new selector.
      - After each event, it checks if the page has navigated (URL changed) and prints a message.
      - Waits 2 seconds after each click.
    """
    filtered_events = deduplicate_events(events)

    script_lines = [
        "from playwright.sync_api import sync_playwright",
        "import re",
        "",
        "# Import self-healing and golden file functions",
        "from self_healer import self_heal, generate_golden_identifier, capture_element_attributes, load_global_golden_data, store_global_golden_data",
        "",
        "def run_test():",
        "    with sync_playwright() as p:",
        "        browser = p.chromium.launch(headless=False)",
        "        page = browser.new_page()",
        f"        page.goto('{website}')",
        "        CURRENT_URL = page.url",
        ""
    ]

    for event in filtered_events:
        if event.get("type") == "click":
            selector = event.get("selector", "")
            if selector:
                script_lines.append(f"        if page.query_selector('{selector}'):")
                script_lines.append(f"            page.click('{selector}')")
                script_lines.append(f"            elem = page.query_selector('{selector}')")
                script_lines.append("            golden_key = generate_golden_identifier(page, '{selector}', elem)")
                script_lines.append("            golden_data = load_global_golden_data()")
                script_lines.append("            golden_data[golden_key] = capture_element_attributes(elem)")
                script_lines.append("            store_global_golden_data(golden_data)")
                script_lines.append("        else:")
                script_lines.append(f"            healed_selector = self_heal('{selector[1:]}', page)")
                script_lines.append("            page.click(healed_selector)")
                script_lines.append("        page.wait_for_timeout(2000)  # Wait 2 seconds")
                script_lines.append("        new_url = page.url")
                script_lines.append("        if new_url != CURRENT_URL:")
                script_lines.append("            CURRENT_URL = new_url")
                script_lines.append("            print('Navigation detected. New URL:', CURRENT_URL)")
        elif event.get("type") == "input":
            selector = event.get("selector", "")
            value = event.get("value", "")
            if selector:
                script_lines.append(f"        if page.query_selector('{selector}'):")
                script_lines.append(f"            page.fill('{selector}', '{value}')")
                script_lines.append(f"            elem = page.query_selector('{selector}')")
                script_lines.append("            golden_key = generate_golden_identifier(page, '{selector}', elem)")
                script_lines.append("            golden_data = load_global_golden_data()")
                script_lines.append("            golden_data[golden_key] = capture_element_attributes(elem)")
                script_lines.append("            store_global_golden_data(golden_data)")
                script_lines.append("        else:")
                script_lines.append(f"            healed_selector = self_heal('{selector[1:]}', page)")
                script_lines.append(f"            page.fill(healed_selector, '{value}')")
                script_lines.append("        new_url = page.url")
                script_lines.append("        if new_url != CURRENT_URL:")
                script_lines.append("            CURRENT_URL = new_url")
                script_lines.append("            print('Navigation detected. New URL:', CURRENT_URL)")

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

        # Listen for console messages that record events.
        page.on("console", handle_console_message)

        # Inject JavaScript to capture click and input events.
        js_code = """
        () => {
            function getSelector(el) {
                if (el.id) {
                    return '#' + el.id;
                }
                if (el.className) {
                    return el.tagName.toLowerCase() + '.' + el.className.split(' ').join('.');
                }
                return el.tagName.toLowerCase();
            }
            document.addEventListener('click', function(event) {
                const selector = getSelector(event.target);
                console.log(JSON.stringify({type: 'click', selector: selector, timestamp: Date.now()}));
            });
            document.addEventListener('input', function(event) {
                const selector = getSelector(event.target);
                console.log(JSON.stringify({type: 'input', selector: selector, value: event.target.value, timestamp: Date.now()}));
            });
        }
        """
        page.evaluate(js_code)

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
