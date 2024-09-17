"use client";

import React, { useState } from "react";
import { LightBulbIcon } from "@heroicons/react/24/solid";
import Link from "next/link";
import Image from "next/image";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";

const CustomNavbar = ({ decodedToken, setDecodedToken, adminUsers }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setDecodedToken(false);
  };

  const navItems = [
    { label: "Home", href: "/" },
    { label: "Dashboard", href: "/dashboard", auth: true },
    { label: "Admin Centre", href: "/admin", admin: true },
  ];

  const drawer = (
    <div className="bg-[#34577E] h-full">
      <div className="p-4">
        <Image
          src="https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?w=150&h=50&fit=crop&crop=edges"
          alt="WattWise Logo"
          width={150}
          height={50}
          className="object-cover"
        />
      </div>
      <List>
        {navItems.map(
          (item) =>
            ((item.auth && decodedToken) ||
              (!item.auth && !item.admin) ||
              (item.admin &&
                decodedToken &&
                adminUsers.includes(decodedToken.email))) && (
              <ListItem
                button
                key={item.label}
                component={Link}
                href={item.href}
              >
                <ListItemText
                  primary={item.label}
                  className="text-[#B8DBD9] hover:text-white transition duration-300"
                />
              </ListItem>
            )
        )}
      </List>
    </div>
  );

  return (
    <AppBar
      position="static"
      className="bg-[#34577E] rounded-b-lg shadow-lg border-b-4 border-[#507DBC]"
    >
      <Toolbar className="justify-between">
        <div className="flex items-center">
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              className="mr-2 text-[#B8DBD9]"
            >
              <MenuIcon />
            </IconButton>
          )}
          <Link href="/" className="flex items-center">
            <LightBulbIcon className="h-8 w-8 text-yellow-500" />
            <span className="ml-2 text-white text-xl font-bold">WattWise</span>
          </Link>
        </div>

        {!isMobile && (
          <div className="flex items-center space-x-4">
            {navItems.map(
              (item) =>
                ((item.auth && decodedToken) ||
                  (!item.auth && !item.admin) ||
                  (item.admin &&
                    decodedToken &&
                    adminUsers.includes(decodedToken.email))) && (
                  <Link
                    key={item.label}
                    href={item.href}
                    className="text-[#B8DBD9] hover:text-white transition duration-300"
                  >
                    {item.label}
                  </Link>
                )
            )}
          </div>
        )}

        <div className="flex items-center space-x-4">
          {decodedToken ? (
            <>
              <Typography variant="body2" className="text-[#B8DBD9]">
                {decodedToken.email}
              </Typography>
              <Button
                onClick={handleLogout}
                className="bg-[#2F4872] hover:bg-[#243A5B] text-white px-4 py-2 rounded transition duration-300"
              >
                Logout
              </Button>
            </>
          ) : (
            <Link
              href="/login"
              className="bg-[#2F4872] hover:bg-[#243A5B] text-white px-4 py-2 rounded transition duration-300"
            >
              Login
            </Link>
          )}
        </div>
      </Toolbar>

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        className="w-64"
      >
        {drawer}
      </Drawer>
    </AppBar>
  );
};

export default CustomNavbar;
