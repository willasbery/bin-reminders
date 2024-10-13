import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons"
import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  Icon,
  Image,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  useBoolean,
} from "@chakra-ui/react"
import { 
  Link as RouterLink,
  createFileRoute, 
  redirect 
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form"

import { emailPattern } from "../utils";
import useAuth, { isLoggedIn } from "../hooks/useAuth"
import { Body_login_access_token_api_v1_login_access_token_post as AccessToken } from "../client";

export const Route = createFileRoute("/login")({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      console.log("User is already logged in"); 
      throw redirect({ to: "/"});
    }
  }
});

function Login() {
  const [show, setShow] = useBoolean()
  const { loginMutation, error, resetError } = useAuth()
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AccessToken>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  }); 

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    if (isSubmitting) return

    resetError()

    try {
      await loginMutation.mutateAsync(data)
    } catch {
      // error is handled by useAuth hook
    }
  }

  return (
    <>
      <Container
        as="form"
        onSubmit={handleSubmit(onSubmit)}
        h="100vh"
        maxW="md"
        alignItems="stretch"
        justifyContent="center"
        gap={4}
        centerContent
      >
        <Text fontSize="3xl" fontWeight="bold" color="ui.main">Bin Collection Reminders</Text>
        <FormControl id="username" isInvalid={!!errors.username || !!error}>
          <Input
            id="username"
            {...register("username", {
              required: "Username is required",
              pattern: emailPattern,
            })}
            placeholder="Email"
            type="email"
            required
          />
          {errors.username && (
            <FormErrorMessage>{errors.username.message}</FormErrorMessage>
          )}
        </FormControl>
        <FormControl id="password" isInvalid={!!error}>
          <InputGroup>
            <Input
              {...register("password", {
                required: "Password is required",
              })}
              type={show ? "text" : "password"}
              placeholder="Password"
              required
            />
            <InputRightElement
              color="ui.dim"
              _hover={{
                cursor: "pointer",
              }}
            >
              <Icon
                as={show ? ViewOffIcon : ViewIcon}
                onClick={setShow.toggle}
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <ViewOffIcon /> : <ViewIcon />}
              </Icon>
            </InputRightElement>
          </InputGroup>
          {error && <FormErrorMessage>{error}</FormErrorMessage>}
        </FormControl>
        <Link as={RouterLink} to="/recover-password" color="ui.main">
          Forgot password?
        </Link>
        <Button variant="primary" type="submit" isLoading={isSubmitting}>
          Log In
        </Button>
        <Text>
          Don't have an account?{" "}
          <Link as={RouterLink} to="/signup" color="ui.main">
            Sign up
          </Link>
        </Text>
      </Container>
    </>
  )
}