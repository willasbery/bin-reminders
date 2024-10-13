import {
  Container, 
  Text, 
  Box,
  Flex
} from '@chakra-ui/react'
import { createFileRoute, redirect } from '@tanstack/react-router'

import useAuth, { isLoggedIn } from '../../hooks/useAuth'


export const Route = createFileRoute("/_layout/profile")({
  component: Profile,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      console.log("User is already logged in"); 
      throw redirect({ to: "/login"});
    }
  }
});


function Profile() {
  const { user: currentUser } = useAuth()
  const reminder_time = currentUser?.reminder_time?.replace("_", " ") || "None"
  
  return (
    <Container maxW="full">
      <Flex justify="center">
        <Box>
          <Text>Hi, {currentUser?.name}, here are your settings</Text>
          <Box>
            <Text>Email: {currentUser?.email}</Text>
            <Text>Phone: {currentUser?.phone_number}</Text>
            <Text>Address: {currentUser?.address}</Text>
            <Text>Preferred contact method: {currentUser?.preferred_contact_method}</Text>
            <Text>Reminder time: {reminder_time}</Text>
          </Box>
        </Box>
        <Box>
          Your next collection is on: 
        </Box>
      </Flex>
    </Container>
  )
}