import { useState, useEffect } from 'react'
import './App.css'
import ContactList from './Contactlist';
import ConactFrom from './ContactForm';

function App() {
  const [contacts, setContacts] = useState([]);
  const [isModelOpen, setIsModelOpen] =  useState(false);
  const [currentContact, setCurrentContact] = useState({})

  useEffect(() => {
    fetchContacts()
  }, []);

  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contact");
    const data = await response.json();
    setContacts(data.contacts);
  };

  const closeModel =()=>{
    setIsModelOpen(false)
    setCurrentContact({})
  }

  const openCreateModel = () => {
    if(!isModelOpen) setIsModelOpen(true)
  }

  const openEditModel = (contact) => {
    if (isModelOpen) return
    setCurrentContact(contact)
    setIsModelOpen(true)
  }

  const onUpdate = () =>{
    closeModel()
    fetchContacts()
  }

  return(
  <>
  <ContactList contacts={contacts} updateContact={openEditModel} updateCallback={onUpdate}/>
  <button onClick={openCreateModel}>create new contanct</button>
  {isModelOpen && <div className='model'>
      <div className='model-content'>
      <span className='close' onClick={closeModel}>&times;</span>
        <ConactFrom exsistingContact={currentContact} updateCallback={onUpdate}/>

      </div>
  </div>

  }
  </>
  );
}

export default App