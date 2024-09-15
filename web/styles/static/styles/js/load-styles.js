fetch("/styles/margin-block").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--padding-block-top", response.margin_top)
    document.documentElement.style.setProperty("--padding-block-bottom", response.margin_bottom)
})

fetch("/styles/colors").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--background-color", response.background_color)
    document.documentElement.style.setProperty("--second-background-color", response.second_background_color)
    document.documentElement.style.setProperty("--main-color", response.main_color)
    document.documentElement.style.setProperty("--secondary-color", response.secondary_color)
})

fetch("/styles/header").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--header-color", response.color)
    document.documentElement.style.setProperty("--header-inverted-color", response.fontColorInverted)
    document.documentElement.style.setProperty("--header-font-family", response.font.name)
    document.documentElement.style.setProperty("--header-font-weight", response.fontWeight)
    document.documentElement.style.setProperty("--header-font-weight-mobile", response.fontWeightMobile)
    document.documentElement.style.setProperty("--header-font-size", response.fontSize)
    document.documentElement.style.setProperty("--header-font-size-mobile", response.fontSizeMobile)
})

fetch("/styles/main-text").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--main-text-color", response.color)
    document.documentElement.style.setProperty("--main-text-inverted-color", response.fontColorInverted)
    document.documentElement.style.setProperty("--main-text-font-family", response.font.name)
    document.documentElement.style.setProperty("--main-text-font-weight", response.fontWeight)
    document.documentElement.style.setProperty("--main-text-font-weight-mobile", response.fontWeightMobile)
    document.documentElement.style.setProperty("--main-text-font-size", response.fontSize)
    document.documentElement.style.setProperty("--main-text-font-size-mobile", response.fontSizeMobile)
})

fetch("/styles/subheader").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--subheader-color", response.color)
    document.documentElement.style.setProperty("--subheader-inverted-color", response.fontColorInverted)
    document.documentElement.style.setProperty("--subheader-font-family", response.font.name)
    document.documentElement.style.setProperty("--subheader-font-weight", response.fontWeight)
    document.documentElement.style.setProperty("--subheader-font-weight-mobile", response.fontWeightMobile)
    document.documentElement.style.setProperty("--subheader-font-size", response.fontSize)
    document.documentElement.style.setProperty("--subheader-font-size-mobile", response.fontSizeMobile)
})

fetch("/styles/explanation-text").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--explanation-text-color", response.color)
    document.documentElement.style.setProperty("--explanation-text-inverted-color", response.fontColorInverted)
    document.documentElement.style.setProperty("--explanation-text-font-family", response.font.name)
    document.documentElement.style.setProperty("--explanation-text-font-weight", response.fontWeight)
    document.documentElement.style.setProperty("--explanation-text-font-weight-mobile", response.fontWeightMobile)
    document.documentElement.style.setProperty("--explanation-text-font-size", response.fontSize)
    document.documentElement.style.setProperty("--explanation-text-font-size-mobile", response.fontSizeMobile)
})

fetch("/styles/icon-size").
then(response => response.json()).
then(response => {
    document.documentElement.style.setProperty("--icon-width", response.width)
    document.documentElement.style.setProperty("--icon-height", response.height)
})
