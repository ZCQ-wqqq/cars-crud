import re

from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


    

def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1. 新建一辆 Honda Civic 2022
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_role("button", name="Create car").click()
    expect(page.get_by_role("heading", name="Honda Civic")).to_be_visible()

    # 2. 点 Edit car，等表单把旧数据填好，再改成 Accord 2023
    page.get_by_role("link", name="Edit car").click()
    expect(page.get_by_label("Model", exact=True)).to_have_value("Civic")
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()

    # 3. 详情页标题变成 Honda Accord
    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible()

    # 4. 刷新后修改依然存在
    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")