import React from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Navbar, Nav, Container, NavDropdown } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../../actions/userActions";
import SearchBox from "../../components/ui/SearchBox";
import logo from "../../img/logo.png";

const Header = () => {
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const dispatch = useDispatch();

  const logoutHandler = () => {
    dispatch(logout());
  };
  return (
    <header>
      <Navbar bg="dark" variant="dark" expand="lg" collapseOnSelect>
        <Container>
          <LinkContainer to="/#">
            <Navbar.Brand>
              <h5>Rhixescans</h5>
              <img
                src={logo}
                alt="Rhixescans"
                width="60"
                height="60"
                className="d-inline-block align-middle"
              />
            </Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <SearchBox />
            <Nav className="ml-auto">
              {userInfo ? (
                <NavDropdown title={userInfo.name} id="username">
                  <LinkContainer to="/profile">
                    <NavDropdown.Item>Profile</NavDropdown.Item>
                  </LinkContainer>

                  <NavDropdown.Item onClick={logoutHandler}>
                    Logout
                  </NavDropdown.Item>
                </NavDropdown>
              ) : (
                <div>
                  <LinkContainer to="/login">
                    <Nav.Link>
                      <i className="fas fa-user"></i>Login
                    </Nav.Link>
                  </LinkContainer>
                  <LinkContainer to="/register">
                    <Nav.Link>
                      <i className="fas fa-user"></i>Register
                    </Nav.Link>
                  </LinkContainer>
                </div>
              )}

              {userInfo && userInfo.isAdmin && (
                <NavDropdown title="Admin" id="adminmenue">
                  <LinkContainer to="/admin/users">
                    <NavDropdown.Item>Users</NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/admin/comics">
                    <NavDropdown.Item>Comics</NavDropdown.Item>
                  </LinkContainer>
                  <LinkContainer to="/admin/chapters">
                    <NavDropdown.Item>Chapters</NavDropdown.Item>
                  </LinkContainer>
                </NavDropdown>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
