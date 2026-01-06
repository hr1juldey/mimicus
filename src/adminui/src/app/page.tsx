"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Activity, Package, Eye, Database, Image, Settings } from "lucide-react";

export default function DashboardPage() {
  const stats = [
    { name: "Total Mocks", value: "24", change: "+2", icon: Package },
    { name: "Active Sessions", value: "12", change: "+1", icon: Database },
    { name: "Requests Today", value: "1,248", change: "+12%", icon: Eye },
    { name: "Active Images", value: "8", change: "+0", icon: Image },
  ];

  const quickActions = [
    { name: "Create New Mock", href: "/mocks/new", icon: Package },
    { name: "View Requests", href: "/inspector", icon: Eye },
    { name: "Manage State", href: "/state", icon: Database },
    { name: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <div className="flex-1 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back! Here's what's happening with your Mimicus instance today.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button asChild>
            <Link href="/mocks/new">Create Mock</Link>
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardDescription className="text-sm font-medium">
                  {stat.name}
                </CardDescription>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">
                  {stat.change} from yesterday
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="lg:col-span-4">
          <CardHeader>
            <CardTitle>Overview</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[200px] flex items-center justify-center text-muted-foreground">
              Chart visualization would go here
            </div>
          </CardContent>
        </Card>
        <Card className="lg:col-span-3">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>
              You made 265 requests this month.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-primary p-2 text-primary-foreground">
                  <Package className="h-4 w-4" />
                </div>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium">New mock created</p>
                  <p className="text-sm text-muted-foreground">users-api</p>
                </div>
                <span className="text-xs text-muted-foreground">10 min ago</span>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-primary p-2 text-primary-foreground">
                  <Eye className="h-4 w-4" />
                </div>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium">Request inspected</p>
                  <p className="text-sm text-muted-foreground">GET /api/users</p>
                </div>
                <span className="text-xs text-muted-foreground">25 min ago</span>
              </div>
              <div className="flex items-center gap-4">
                <div className="rounded-full bg-primary p-2 text-primary-foreground">
                  <Database className="h-4 w-4" />
                </div>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-medium">State updated</p>
                  <p className="text-sm text-muted-foreground">session-123</p>
                </div>
                <span className="text-xs text-muted-foreground">1 hour ago</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => {
            const Icon = action.icon;
            return (
              <Link key={index} href={action.href}>
                <Card className="hover:bg-muted/50 transition-colors cursor-pointer">
                  <CardHeader className="flex flex-row items-center gap-4">
                    <div className="rounded-lg bg-primary p-2 text-primary-foreground">
                      <Icon className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-lg">{action.name}</CardTitle>
                    </div>
                  </CardHeader>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}