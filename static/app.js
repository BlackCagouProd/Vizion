

$.ajax({
    url: "/",
    success: display_news
});


function display_news(result) {
    console.log("Résultat de la requête :", result);
    news_data = result["data"];

}