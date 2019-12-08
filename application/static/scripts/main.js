import React from 'react';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import FootGrid from './foot_grid.js'


export default function MainPanel() {
  return (
    <Container maxWidth="sm">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Moustache Maker
        </Typography>
        <FootGrid />
      </Box>

    </Container>
  );
}