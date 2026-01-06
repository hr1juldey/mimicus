// src/app/images/page.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function ImagesPage() {
  const [imageSize, setImageSize] = useState({ width: 300, height: 200 });
  const [imageUrl, setImageUrl] = useState('');

  const handleGenerateImage = () => {
    // In a real app, this would call an API to generate an image
    setImageUrl(`https://placehold.co/${imageSize.width}x${imageSize.height}/000000/FFFFFF?text=Mimicus+Image`);
  };

  const handleDevicePreset = (width: number, height: number) => {
    setImageSize({ width, height });
    setImageUrl(`https://placehold.co/${width}x${height}/000000/FFFFFF?text=${width}x${height}`);
  };

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Image Management</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Generate Placeholder Image</CardTitle>
              <CardDescription>Create placeholder images for your mocks</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Width (px)</label>
                  <Input
                    type="number"
                    value={imageSize.width}
                    onChange={(e) => setImageSize({...imageSize, width: parseInt(e.target.value) || 0})}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Height (px)</label>
                  <Input
                    type="number"
                    value={imageSize.height}
                    onChange={(e) => setImageSize({...imageSize, height: parseInt(e.target.value) || 0})}
                  />
                </div>
              </div>
              
              <Button onClick={handleGenerateImage} className="w-full">
                Generate Image
              </Button>
              
              {imageUrl && (
                <div className="mt-4">
                  <img 
                    src={imageUrl} 
                    alt="Generated placeholder" 
                    className="w-full border rounded"
                  />
                  <div className="mt-2 flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => navigator.clipboard.writeText(imageUrl)}>
                      Copy URL
                    </Button>
                    <Button variant="outline" size="sm">
                      Download
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Upload Image</CardTitle>
              <CardDescription>Upload your own images to use in mocks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <p className="mb-4">Drag and drop your image here, or click to browse</p>
                <Button variant="outline">Select File</Button>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Device Presets</CardTitle>
              <CardDescription>Common device resolutions</CardDescription>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-2">
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(375, 667)}
              >
                iPhone SE
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(375, 812)}
              >
                iPhone 12
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(768, 1024)}
              >
                iPad
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(1920, 1080)}
              >
                Desktop
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(1366, 768)}
              >
                Laptop
              </Button>
              <Button 
                variant="outline" 
                size="sm"
                onClick={() => handleDevicePreset(360, 640)}
              >
                Android
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Images</CardTitle>
              <CardDescription>Your recently generated images</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[1, 2, 3].map((item) => (
                  <div key={item} className="flex items-center gap-3 p-2 border rounded">
                    <div className="bg-gray-200 border rounded w-16 h-16" />
                    <div className="flex-1">
                      <div className="text-sm font-medium">Placeholder-{item}.png</div>
                      <div className="text-xs text-muted-foreground">300×200</div>
                    </div>
                    <Button variant="outline" size="sm">Use</Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Image Gallery</CardTitle>
              <CardDescription>All your uploaded images</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-2">
                {[1, 2, 3, 4, 5, 6].map((item) => (
                  <div key={item} className="aspect-square bg-gray-200 border rounded" />
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}