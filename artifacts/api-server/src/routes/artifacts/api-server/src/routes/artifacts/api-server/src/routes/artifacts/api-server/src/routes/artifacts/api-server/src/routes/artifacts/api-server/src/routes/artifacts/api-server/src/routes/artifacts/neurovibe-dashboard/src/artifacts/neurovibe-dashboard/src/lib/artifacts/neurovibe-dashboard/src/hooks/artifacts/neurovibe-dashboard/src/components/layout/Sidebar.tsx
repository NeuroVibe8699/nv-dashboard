import { Link, useLocation } from "wouter";
import { LayoutDashboard, Server, MapPin, Users, Bell, LogOut } from "lucide-react";
import { useAuth } from "@/lib/auth";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }

export function Sidebar() {
  const [location] = useLocation();
  const { user, signOut } = useAuth();

  const links = [
    { href: "/", label: "Dashboard", icon: LayoutDashboard },
    { href: "/devices", label: "Device Inventory", icon: Server },
    { href: "/sites", label: "Sites", icon: MapPin },
    { href: "/alerts", label: "Alerts", icon: Bell },
  ];
  if (user?.role === "admin") links.push({ href: "/users", label: "Users", icon: Users });

  return (
    <div className="w-64 bg-card/80 backdrop-blur-xl border-r border-border h-screen flex flex-col fixed left-0 top-0 z-40">
      <div className="p-6 flex items-center gap-3">
        <img src={`${import.meta.env.BASE_URL}images/logo.png`} alt="NeuroVibe Logo" className="w-8 h-8" />
        <div>
          <h1 className="font-display font-bold text-lg text-foreground tracking-wide leading-none">NeuroVibe</h1>
          <p className="text-[10px] text-primary uppercase tracking-widest font-semibold mt-1">AI Predictive</p>
        </div>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4 overflow-y-auto">
        {links.map((link) => {
          const isActive = location === link.href || (link.href !== '/' && location.startsWith(link.href));
          return (
            <Link key={link.href} href={link.href} className={cn(
              "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 font-medium text-sm group",
              isActive
                ? "text-primary-foreground bg-primary shadow-[0_0_20px_rgba(59,130,246,0.3)]"
                : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
            )}>
              <link.icon className={cn("w-5 h-5", isActive ? "scale-110" : "group-hover:scale-110")} />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border/50">
        <div className="bg-secondary/30 rounded-xl p-4 mb-4 border border-border/50 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary/20 text-primary flex items-center justify-center font-display font-bold">
            {user?.fullName.charAt(0).toUpperCase()}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-bold text-foreground truncate">{user?.fullName}</p>
            <p **...**

_This response is too long to display in full._
