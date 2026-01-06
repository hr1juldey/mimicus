// src/app/mocks/page.tsx
"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { apiClient } from "@/lib/api-client";
import { MockDefinition } from "@/types/api";
import Link from "next/link";

export default function MocksPage() {
  const [mocks, setMocks] = useState<MockDefinition[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMocks();
  }, []);

  const fetchMocks = async () => {
    try {
      setLoading(true);
      const data = await apiClient.get<MockDefinition[]>('/api/admin/mocks');
      setMocks(data);
    } catch (error) {
      console.error('Error fetching mocks:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-10">
        <p>Loading mocks...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Manage Mocks</h1>
        <Button asChild>
          <Link href="/mocks/new">Create New Mock</Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mocks.map((mock) => (
          <Card key={mock.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-lg">{mock.name}</CardTitle>
                <Badge variant={mock.enabled ? "default" : "secondary"}>
                  {mock.enabled ? "Active" : "Inactive"}
                </Badge>
              </div>
              <CardDescription>
                {mock.match.method} {mock.match.path}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p className="text-sm">
                  <span className="font-medium">Mode:</span> {mock.mode}
                </p>
                <p className="text-sm">
                  <span className="font-medium">Status:</span> {mock.response.status}
                </p>
                <p className="text-sm">
                  <span className="font-medium">Priority:</span> {mock.priority}
                </p>
              </div>
              <div className="flex gap-2 mt-4">
                <Button variant="outline" size="sm" asChild>
                  <Link href={`/mocks/${mock.id}`}>Edit</Link>
                </Button>
                <Button variant="outline" size="sm">Test</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}