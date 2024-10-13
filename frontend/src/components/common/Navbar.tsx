import {
  background,
  Button,
  Flex,
  Heading,
  Link,
  Stack,
} from "@chakra-ui/react";
import type { ParsedLocation } from "@tanstack/react-router";
import { Link as RouterLink, useRouterState } from "@tanstack/react-router";
import useAuth, { isLoggedIn } from "../../hooks/useAuth";

const Navbar = () => {
  const currentRoute = useRouterState({
    select: (state) => state.location
  });

  return (
    <Flex 
      as="nav" 
      w="100%"
      h="10vh"
      justify="space-between" 
      padding="1.5rem" 
      bg="ui.main" 
      color="white"
    >
      <Flex align="center" mr={5}>
        <Heading as="h1" size="lg" letterSpacing={"-.1rem"}>
          <Link as={RouterLink} to="/" color="white">
            Bin Collection
          </Link>
        </Heading>
      </Flex>
      {isLoggedIn() ? <LoggedInNavbar currentRoute={currentRoute} /> : <NotLoggedInNavbar currentRoute={currentRoute} />}
    </Flex>
  );
}

interface NavbarProps {
  currentRoute: ParsedLocation<any>;
}

function LoggedInNavbar({ currentRoute }: NavbarProps) {
  const { logout } = useAuth();

  const handleLogout = async () => {
    logout()
  }

  return (
    <Stack direction="row" spacing={4}>
      <NavLink to="/profile" currentRoute={currentRoute}>Profile</NavLink>
      <Button 
        onClick={handleLogout}
        backgroundColor={"ui.main"}
        color={"ui.light"}
        _hover={{
          backgroundColor: "ui.light",
          color: "ui.main",
        }}
      >
        Logout
      </Button>
    </Stack>
  );
}

function NotLoggedInNavbar({ currentRoute }: NavbarProps) {
  return (
    <Stack direction="row" spacing={4}>
      <NavLink to="/login" currentRoute={currentRoute}>Login</NavLink>
      <NavLink to="/register" currentRoute={currentRoute}>Register</NavLink>
    </Stack>
  );
}

interface NavLinkProps {
  to: string;
  currentRoute: ParsedLocation<any>;
  children: React.ReactNode;
}

function NavLink({ to, currentRoute, children }: NavLinkProps) {
  const isActive = currentRoute.pathname === to;

  return (
    <Button 
      as={RouterLink}
      to={to}
      backgroundColor={isActive ? "ui.main" : "ui.secondary"}
      border={isActive ? "2px solid" : "none"}
      color={isActive ? "ui.light" : "ui.main"}
      _hover={{
        backgroundColor: "ui.light",
        color: "ui.main",
      }}
    >
      {children}
    </Button>
  );
}

export default Navbar;
