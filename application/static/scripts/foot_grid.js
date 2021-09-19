import React from 'react';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import Link from '@material-ui/core/Link';

function Copyright(props) {
  console.log("copyright");
  return (
    <Typography variant="body2" color="textSecondary" align="center" nowrap="true" p={props.padding} m={props.margin}>
      {'Copyright © '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

function Contact(props) {
  console.log("contact");
  return (
    <Typography variant="body2" color="textPrimary" align="center" nowrap="true">
      {"Email "}
      <Link color="inherit" href="mailto:collinsconway@gmail.com">
        collinsconway@gmail.com
      </Link>
    </Typography>

  );
}

function Github(props) {
  console.log("github");
  return (
    <Typography variant="body2" color="textPrimary" align="center" nowrap="true">
      {"Github "}
      <Link color="inherit" href="https://github.com/collinsc/MoustacheMaker">
        github.com/collinsc/MoustacheMaker
      </Link>

    </Typography>
  );
}


export default function FootGrid() {
  console.log("grid");

  return(
    <div>
      <Box display= "flex" flexWrap="wrap" justifyContent="space-around"> 
        <Contact />
        {"|"}
        <Github />
      </Box>
      <Copyright/>
    </div>
  );
}
