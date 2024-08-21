document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', send_email)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    emails.forEach(email => {
      console.log(email)
      const emailDiv = document.createElement('div')
      emailDiv.innerHTML = `
          <h4>Sender: ${email.sender}</h4>
          <h4>Subject: ${email.subject}</h4>
          <p>Timestamp: ${email.timestamp}</p>
        `
      emailDiv.style.border = '1px solid #ccc';
      emailDiv.style.padding = '10px';
      emailDiv.style.margin = '10px 0';
      emailDiv.style.cursor = 'pointer';
      emailDiv.addEventListener('click', () => load_email(email.id));
      document.querySelector('#emails-view').append(emailDiv);
    })
});
}

function load_email(email_id) {
  // Fetch the email details from the server
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      // Show the email view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';

      // Create a container for the email details
      const emailDetailView = document.createElement('div');
      emailDetailView.innerHTML = `
        <h3><strong>From:</strong> ${email.sender}</h3>
        <h3><strong>To:</strong> ${email.recipients.join(', ')}</h3>
        <h3><strong>Subject:</strong> ${email.subject}</h3>
        <p><strong>Timestamp:</strong> ${email.timestamp}</p>
        <hr>
        <p>${email.body}</p>
      `;
      emailDetailView.style.border = '1px solid #ccc';
      emailDetailView.style.padding = '10px';
      emailDetailView.style.margin = '10px 0';

      // Clear out the emails view and append the email details
      const emailsView = document.querySelector('#emails-view')
      emailsView.innerHTML = ''; // Clear the previous content
      emailsView.append(emailDetailView);
      emailsView.style.display = 'block'; // Show the email details view

      // Mark the email as read if it is not already read
      if (!email.read) {
        fetch(`/emails/${email.email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }
      const archiveButton = document.createElement('button')
      archiveButton.innerHTML = email.archived ? 'Unarchive' : 'Archive'
      archiveButton.className = email.archived ? 'btn btn-success' : 'btn btn-danger'

      // Add event listener to handle archiving/unarchiving
      archiveButton.addEventListener('click', function() {
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: !email.archived
          })
        })
        .then(() => {
          // Reload the mailbox after archiving/unarchiving
          load_mailbox('inbox');
        });
      });

      // Append the button to the email details view
      emailDetailView.append(archiveButton);

      const replyButton = document.createElement('button')
      replyButton.innerHTML = 'Reply'
      replyButton.className = 'btn btn-info'
      replyButton.addEventListener('click', function(){
        compose_email()
        document.querySelector('#compose-recipients').value = email.sender
        let subject = email.subject
        if (subject.split(' ',1)[0] !== "Re:"){
          subject = "Re: " + email.subject
        }
        document.querySelector('#compose-subject').value = subject
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote `
        // document.querySelector('#emails-view').style.display = 'none';
        // document.querySelector('#compose-view').style.display = 'block';

        // // Pre-fill composition form
        // document.querySelector('#compose-recipients').value = email.sender;
        // document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
        // document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
      })
      emailDetailView.append(replyButton)
    })
}


function send_email(event) {
    event.preventDefault();

    const recipients = document.querySelector("#compose-recipients").value
    const subjects = document.querySelector("#compose-subject").value
    const body = document.querySelector("#compose-body").value
    console.log('send email')

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subjects,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        load_mailbox('sent')
    });
}