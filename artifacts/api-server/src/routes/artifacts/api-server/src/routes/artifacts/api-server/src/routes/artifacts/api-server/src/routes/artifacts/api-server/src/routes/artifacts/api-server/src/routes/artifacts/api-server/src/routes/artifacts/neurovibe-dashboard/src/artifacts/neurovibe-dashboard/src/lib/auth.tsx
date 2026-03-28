import React, { createContext, useContext, useState, useEffect } from "react";
import { User, LoginRequest, login } from "@workspace/api-client-react";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  signIn: (credentials: LoginRequest) => Promise<void>;
  signOut: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem("neurovibe_user");
    const storedToken = localStorage.getItem("neurovibe_token");
    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
    }
    setIsLoading(false);
  }, []);

  const signIn = async (credentials: LoginRequest) => {
    try {
      const response = await login(credentials);
      setUser(response.user);
      if (response.token) {
        setToken(response.token);
        localStorage.setItem("neurovibe_token", response.token);
      }
      localStorage.setItem("neurovibe_user", JSON.stringify(response.user));
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  };

  const signOut = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("neurovibe_user");
    localStorage.removeItem("neurovibe_token");
    window.location.href = "/login";
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
