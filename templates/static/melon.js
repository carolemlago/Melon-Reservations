'use strict';

// Create Calendar

document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    
    // AJAX request
    fetch('/get_calendar_events')
      .then(response => response.json())
      .then(responseData => {
        const today = new Date().toJSON().slice(0,10);
    
        const calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          initialDate: today,
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
          },
          
          height: "auto",
          events: responseData
        });
      
      calendar.render();
      });
      });

//   Delete Appointment

const deleteButton = document.querySelectorAll('.delete');

for (let i = 0; i < deleteButton.length; i++) {
    const handleClickDelete = (evt) => {
    // Delete event from dashboard
      
    const formInputs = {
      reservationId: document.getElementById(`reservation-id${i}`).value,
    };
    
    fetch('/delete_appointment', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.text())
      .then((responseData) => {
        document.querySelector(`#reservation-div${i}`).remove();
        document.querySelector(`#reservation-div${i}`).style.display ='none';
        
        alert('Your appointment is deleted!');
      });

    }
  deleteButton[`${i}`].addEventListener('click', handleClickDelete);
}