"use client";

import { Home, Settings, Eye, Database, Image, Package, Activity, BarChart3, Users, Server } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const navItems = [
  { href: "/", label: "Dashboard", icon: BarChart3, badge: null },
  { href: "/mocks", label: "Mocks", icon: Package, badge: "12" },
  { href: "/inspector", label: "Inspector", icon: Eye, badge: "24" },
  { href: "/state", label: "State", icon: Database, badge: null },
  { href: "/images", label: "Images", icon: Image, badge: null },
  { href: "/settings", label: "Settings", icon: Settings, badge: null },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-50 hidden w-64 border-r bg-background md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <div className="h-8 w-8 rounded-md bg-primary flex items-center justify-center">
              <span className="text-white font-bold text-sm">M</span>
            </div>
            <span className="">Mimicus</span>
          </Link>
        </div>

        <div className="flex-1">
          <nav className="grid items-start gap-1 px-2 text-sm font-medium lg:px-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary ${
                    isActive
                      ? "bg-muted text-primary"
                      : "text-muted-foreground hover:bg-muted"
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {item.label}
                  {item.badge && (
                    <Badge
                      variant="secondary"
                      className="ml-auto flex h-6 w-6 shrink-0 items-center justify-center"
                    >
                      {item.badge}
                    </Badge>
                  )}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="mt-auto p-4 border-t">
          <div className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-colors hover:text-primary">
            <Activity className="h-5 w-5" />
            <span className="text-sm">System Status</span>
            <Badge variant="outline" className="ml-auto">Online</Badge>
          </div>
        </div>
      </div>
    </aside>
  );
}