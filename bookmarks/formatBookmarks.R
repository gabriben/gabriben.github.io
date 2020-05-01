library(rvest)
library(dplyr)

page <- read_html("Safari Bookmarks.html") 


page %>% html_nodes(".vcard .name") %>% html_text()

tibble(
  name = page %>% html_nodes(".vcard .name") %>% html_text(),
  address = page %>% html_nodes(".vcard .address") %>% html_text(),
  type = page %>% html_nodes(".vcard .brewery_type") %>% html_text() %>% stringr::str_replace_all("^Type: ", ""),
  website = page %>% html_nodes(".vcard .url a") %>% html_attr("href")
)


read
