"""
https://poe.com/chat/3e1jw21901csun1xix4






async def set_location(latitude, longitude):
    browser = await launch()
    page = await browser.newPage()

    # 设置地理位置
    await page.emulateMediaFeatures([{
        'name': 'geolocation',
        'value': f'{{ "latitude": {latitude}, "longitude": {longitude} }}'
    }])

    # 导航到需要的页面
    await page.goto('https://www.example.com')

    # 执行其他操作...

    await browser.close()


# 调用函数设置位置
await set_location(37.7749, -122.4194)  # 设置位置为旧金山"

"""
