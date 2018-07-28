#importing libraries
library(shiny)
library(shinydashboard)
library(dplyr)
library(ggplot2)
library(plotly)
require(plotly)
library(leaflet)
library(DT)


#Reading csv file
house <- read.csv("house.csv",header = T,stringsAsFactors = F)
hDat <- house
hDat$id <- seq.int(nrow(hDat))

##############################################################################
# UI Side
##############################################################################
#creating shiny Dashboard

ui <- shinyUI(dashboardPage(
  dashboardHeader(title = "Melbourne Housing"),
  dashboardSidebar(
    #Sidebar Menu with submenu items
    sidebarMenu(id='sidebar',
                menuItem("Introduction",tabName = "introduction", icon = icon("dashboard")),
                menuSubItem("Suburbs", tabName = "Suburbs", icon = icon("map-marker")),
                menuSubItem("HouseType", tabName = "HouseType", icon = icon("home")),
                menuSubItem("Distance from CBD",tabName = "CBD", icon = icon("align-justify")),
                menuSubItem("Housing", tabName = "Housing", icon = icon("align-justify")),
                menuSubItem("Overview", tabName = "Overview", icon = icon("th"))
                #menuSubItem("Building", tabName = "Building", icon = icon("align-justify")),
                
                
    ), 
    
    conditionalPanel("input.sidebar=='Housing'",
                     fluidRow(sliderInput(
                       inputId = "price",
                       label="Show variation in price", 
                       min=min(hDat$Price), max=max(hDat$Price),
                       value=c(min(hDat$Price),max(hDat$Price))
                     ))
    ),
    conditionalPanel("input.tabs=='CBD'",
                     fluidRow()
                     
    )),
  
  dashboardBody(
    
    tabItems(
      
      tabItem(tabName = "Housing",h3('Melbourne Housing Data'), leafletOutput('map01'), dataTableOutput('table01')),
      
      tabItem(tabName = "Suburbs", h3('Clustering of Suburbs'),leafletOutput("map1"),actionButton("add", "Add Marker cluster"),actionButton("clear", "Clear marker cluster")),
      tabItem(tabName = "introduction",h3("INTRODUCTION"),br(), h4("Melbourne is the second most populous city in Australia and it is ranked the world's most liveable city. The housing market in Melbourne is 
                                           changing rapidly, before you think of moving to Melbourne, you should see this!"), 
              br(), h4("In this webpage, I have created visualizations that provide different kinds of information about the housing market in Melbourne. The data for these visualizations were extracted from the dataset melbourne_housing_data, which contains 17.408 randomly sampled and geocoded house sales for the last 6 months in Melbourne."),
              br(), h4("To see the first visualization scroll down or click on the next tab below")),
      tabItem(tabName = "CBD", h3("Distance From CBD"),leafletOutput("mydistance"), title = h3("Distance From CBD"), sliderInput("sliderDistance", "Distance Slider", value = range(house$Distance), min = min(house$Distance), max = max(house$Distance))),
      tabItem(tabName = "Building", h2("Building sizes"), leafletOutput("mybuilding")),
      tabItem(tabName = "Overview", h3('Find a house'),leafletOutput("mysuburb1"),uiOutput('house1'), sliderInput("pslider",h3("Price"), round = TRUE, value = range(house$Price), min = min(house$Price), max = max(house$Price)),  
              sliderInput("sliderDist", h3("Distance"), value = range(house$Distance), min = min(house$Distance), max = max(house$Distance)),
              radioButtons("dist", h3("House type:"), c("HOUSE, COTTAGE, VILLA, TERRACE" = "h",
                                                    "UNIT, DUPLEX" = "u",
                                                    "TOWN HOUSE" = "t"), selected = NULL, inline = TRUE),
              #div(style="display: inline-block;vertical-align:top; width: 150px;",selectInput('Bathroom', 'Select Bathroom', choices=unique(house[which(house$Car >= input$cars & house$Rooms >= input$Rooms), ]$Bathroom), selectize = FALSE)),
              div(style="display: inline-block;vertical-align:top; width: 350px;",selectInput('suburb', 'Suburbs', choices=unique(house$Suburb), multiple = TRUE)),
              div(style="display: inline-block;vertical-align:top; width: 150px;",selectInput('Bed', 'Bedrooms - eg 1+', choices=sort(as.numeric(unique(house$Bedroom2))), selectize = FALSE)),
              div(style="display: inline-block;vertical-align:top; width: 150px;",selectInput('cars', 'Cars', choices=sort(as.numeric(unique(house$Car))), selectize = FALSE)),
              #selectInput('suburb', 'Suburbs', choices=unique(house$Suburb), multiple = TRUE),
              div(style="display: inline-block;vertical-align:top; width: 150px;",selectInput('Rooms', 'Rooms', choices=sort(as.numeric(unique(house$Rooms))), selectize = FALSE))),
      #selectInput('Bathrooms', 'Bathrooms', c(Choose='', sort(as.numeric(unique(house$Bathroom)))), selectize=FALSE)),
      #tabItem(tabName = "Suburbs", h2("Suburb Data"), leafletOutput("mysuburb"), sliderInput("pslider",h3("Price Slider"), round = TRUE, value = range(house$Price), min = min(house$Price), max = max(house$Price)), sliderInput("sliderDist", "Distance Slider", value = range(house$Distance), min = min(house$Distance), max = max(house$Distance))),
      tabItem(tabName = "HouseType",h2("Housetype Category"),leafletOutput("myhousetypee"), radioButtons("dist1", "House type:",
                                                                                                         c("HOUSE, COTTAGE, VILLA, TERRACE" = "h",
                                                                                                           "UNIT, DUPLEX" = "u",
                                                                                                           "TOWN HOUSE" = "t")))
      
      
      )
  ) 
  ))

##############################################################################
# Server Side
##############################################################################

server <- function(input, output, session){
  
  #creating a subset of data
  qSub <-  reactive({
    
    subset <- subset(hDat, hDat$Price>=input$price[1] &
                       hDat$Price<=input$price[2]) %>% head(25)
  })
  
  # display 10 rows initially of data table
  output$table01 <- DT::renderDataTable(
    DT::datatable(house, options = list(pageLength = 25))
  )
  
  
  # to keep track of previously selected row
  prev_row <- reactiveVal()
  
  #Display custom icons
  my_icon = makeAwesomeIcon(icon = 'flag', markerColor = 'red', iconColor = 'white')
  
  
  #code for housing tab
  observeEvent(input$table01_rows_selected, {
    row_selected = qSub()[input$table01_rows_selected,]
    proxy <- leafletProxy('map01')
    print(row_selected)
    proxy %>%
      addAwesomeMarkers(popup=as.character(row_selected$Price),
                        layerId = as.character(row_selected$id),
                        lng=row_selected$long, 
                        lat=row_selected$lat,
                        icon = my_icon)
    
    # Reset previously selected marker
    if(!is.null(prev_row()))
    {
      proxy %>%
        addMarkers(popup=as.character(prev_row()$Price), 
                   layerId = as.character(prev_row()$id),
                   lng=as.numeric(prev_row()$long), 
                   lat=as.numeric(prev_row()$lat))
    }
    # set new value to reactiveVal 
    prev_row(row_selected)
  })
  
  output$map01 <- renderLeaflet({
    
    #color code for legend
    pal <- colorNumeric("YlOrRd", domain=c(min(house$Price), max(house$Price)))
    qMap <- leaflet(data = qSub()) %>% 
      addTiles() %>%
      addMarkers(popup=paste0("Price : ", ~as.character(Price)), layerId = as.character(qSub()$id)) %>%
      addLegend("bottomright", pal = pal, values = ~Price,
                title = "Price Magnitude",
                opacity = 1)
    qMap
  })
  
  # datatable rows
  observeEvent(input$map01_marker_click, {
    clickId <- input$map01_marker_click$id
    dataTableProxy("table01") %>%
      selectRows(which(qSub()$id == clickId)) %>%
      selectPage(which(input$table01_rows_all == clickId) %/% input$table01_state$length + 1)
  })
  
  
  
  output$map1 <- renderLeaflet({
    #house <- house %>% filter(Price > input$slider[1] & Price < input$slider[2])
    center_lon = median(house$long)
    center_lat = median(house$lat)
    leaflet(house) %>% addTiles() %>% setView(lng=center_lon, lat=center_lat, zoom=12)
    
  })
  
  #creating clusters of suburbs
  observeEvent(input$add, {
    
    leafletProxy("map1") %>% addMarkers(lng = house$long, lat = house$lat,
                                        data = house,
                                        popup = ~paste("Price :", house$Price,"<br>", "Suburb : ", house$Suburb, "<br>", "Address : ", house$Address), layerId = rownames(house),
                                        clusterOptions = markerClusterOptions(), clusterId = "cluster1"
    )
  })
  
  # Code for clustering suburbs
  observeEvent(input$clear, {
    leafletProxy("map1") %>% clearMarkerClusters()
  })
  observe({
    leafletProxy("map1") %>% removeMarkerFromCluster(input$remove1, "cluster1")
  })
  observe({
    print(input$map1_marker_click)
  })
  
  
  output$mydistance <- renderLeaflet({ 
    
    temp <- house %>% filter(Distance > input$sliderDistance[1] & Distance < input$sliderDistance[2])
    temp <- na.omit(temp)
    center_lon = median(temp$long)
    center_lat = median(temp$lat)
    
    leaflet(house$Distance) %>% addTiles() %>%
      addCircles(lng = ~long, lat = ~lat, data = temp, layerId = temp$Distance, radius = 7, popup = paste0("Distance : ", as.character(temp$Distance), "<br>",
                                                                                                           "Price : ", as.character(temp$Price), "<br>",
                                                                                                           "Suburb : ", as.character(temp$Suburb)),
                 color = c("red"))  %>%
      
      # controls
      setView(lng=center_lon, lat=center_lat, zoom=12)
  })
  
  #Code for displaying housetype
  output$myhousetypee <- renderLeaflet({ 
    temp <- house %>% filter(Type == input$dist1)
    temp <- na.omit(temp)
    
    center_lon = median(temp$long)
    center_lat = median(temp$lat)
    
    #color combination for different types of house
    mcol = c()
    if(input$dist1 == "h")
    {mcol = "red"}
    if(input$dist1 == "u")
    {mcol = "green"}
    if(input$dist1 == "t")
    {mcol = "blue"}
    
    #plotting map
    leaflet(house$Type) %>% addTiles() %>%
      addMarkers(lng = ~long, lat = ~lat, data = temp, popup = paste("Bedroom : ", as.character(temp$Bedroom2), "<br>",
                                                                                       "Bathroom : ", as.character(temp$Bathroom), "<br>",
                                                                                       "Rooms: ", as.character(temp$Rooms), "<br>",
                                                                                      "Type: ", as.character(temp$Type), "<br>",
                                                                                       "Cars : ", as.character(temp$Car))
                       )  %>%
      
      # controls
      setView(lng=center_lon, lat=center_lat, zoom=12)})

  
  
  output$house1<-renderUI({
    selectInput('Bathroom', 'Select Bathroom', choices=sort(unique(house[which(house$Car >= input$cars & house$Rooms >= input$Rooms), ]$Bathroom)), selectize = FALSE)
  })
  
  
  
  output$mysuburb1 <- renderLeaflet({
    
    validate(
      need(!is.null(input$Bathroom),""),
      need(!is.null(input$cars),"")
    )
    
    center_lon = median(house$long)
    center_lat = median(house$lat)
    
    
    #filtering the dataset based on the user input
    house <- house %>% filter(Price > input$pslider[1] & Price < input$pslider[2])
    house <- house %>% filter(Distance > input$sliderDist[1] & Distance < input$sliderDist[2])
    house <- house %>% filter(Type %in% input$dist)
    house <- house %>% filter(Suburb %in% input$suburb)
    house <- filter(house, Car >= input$cars, Bathroom >= input$Bathroom, Rooms >= input$Rooms, Bedroom2 >= input$Bed)    
    
    #Plotting the map
    m <-leaflet() %>% addTiles() %>%
      addMarkers(lng = ~long, lat = ~lat, data = house,
                 popup = paste("Price : ", as.character(house$Price), "<br>",
                               "Suburb : ", as.character(house$Suburb), "<br>",
                               "Cars : ", as.character(house$Car),"<br>",
                               "Bathroom : ", as.character(house$Bathroom), "<br>",
                               "Rooms : ", as.character(house$Rooms), "<br>",
                               "Bedrooms : ", as.character(house$Bedroom2),"<br>"
                 ))  %>%
      #addMarkers(data = school, popup = as.character(school$Schools, school$ICSEA.Rank), clusterOptions = markerClusterOptions()) %>%
      
      # controls
      setView(lng=center_lon, lat=center_lat, zoom=12)
    
  })
  
  
}
#Running the app
shinyApp(ui, server)

