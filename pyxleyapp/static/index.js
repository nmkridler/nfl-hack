
    import React from 'react';
    import ReactDOM from 'react-dom';
    import { Router, Route, Link, browserHistory } from 'react-router';

    
    import Main from './layout.js';
    

    ReactDOM.render(
      <Router history={ browserHistory }>
      
      <Route path='/' component={ Main } />
      
      </Router>,
      document.getElementById("component_id")
    );

    