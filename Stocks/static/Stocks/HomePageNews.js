function changeNewsTab(button_id, container_id){

    let buttons = document.getElementsByClassName("tabButton");
    const length = buttons.length;

    //Get all elements with class 'tabButton' and remove the class 'Active'
    for(let i = 0; i <length; i++){
        buttons[i].className = buttons[i].className.replace('Active', '');
    }

    //Get all containers and hide their contents
    let containers = document.getElementsByClassName('tabcontent');
    const length1 = containers.length;
    for(let j = 0; j <length1; j++){
        containers[j].style.display = 'none';
    }

    //Set the active button
    document.getElementById(button_id).className += ' Active';
    document.getElementById(container_id).style.display = 'block';


}