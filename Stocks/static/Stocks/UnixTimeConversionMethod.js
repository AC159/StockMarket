function Convert(){

    let dates = document.getElementsByClassName("date");
    const length = dates.length;

    for(let i = 0; i < length; i++){

        dates[i].innerHTML = TimeConverter(dates[i].innerHTML);

    }


}

function TimeConverter(UnixTimeStamp){

    let date = new Date(UnixTimeStamp * 1000); //Convert unix time to milliseconds instead of seconds as it originally is.

    let day = date.getDate(); //Day of the month (1-31)

    let month = date.getMonth(); //Month of the year (1-12)

    let year = date.getFullYear(); //Year we are in

    //Return the date in Month-Day-Year format
    return `${month}-${day}-${year}`;

}