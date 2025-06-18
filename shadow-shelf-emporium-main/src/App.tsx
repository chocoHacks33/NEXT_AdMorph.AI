import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from "react";
import Index from "./pages/Index";
import Cart from "./pages/Cart";
import ProductDetail from "./pages/ProductDetail";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import { CartItemType } from "./components/CartItem";
import { Product } from "./components/ProductCard";
import { AuthProvider } from "./contexts/AuthContext";

const queryClient = new QueryClient();

const App = () => {
  const [cartItems, setCartItems] = useState<CartItemType[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  const handleUpdateQuantity = (id: number, quantity: number) => {
    if (quantity === 0) {
      setCartItems(prevItems => prevItems.filter(item => item.id !== id));
    } else {
      setCartItems(prevItems =>
        prevItems.map(item =>
          item.id === id ? { ...item, quantity } : item
        )
      );
    }
  };

  const handleRemoveItem = (id: number) => {
    setCartItems(prevItems => prevItems.filter(item => item.id !== id));
  };

  const handleAddToCart = (product: Product) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);
      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevItems, { ...product, quantity: 1 }];
      }
    });
  };

  const totalCartItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <AuthProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route 
                path="/" 
                element={
                  <Index 
                    cartItems={totalCartItems}
                    onAddToCart={handleAddToCart}
                    onProductSelect={setSelectedProduct}
                  />
                } 
              />
              <Route 
                path="/cart" 
                element={
                  <Cart 
                    cartItems={cartItems}
                    onUpdateQuantity={handleUpdateQuantity}
                    onRemoveItem={handleRemoveItem}
                  />
                } 
              />
              <Route 
                path="/product" 
                element={
                  <ProductDetail 
                    product={selectedProduct}
                    onAddToCart={handleAddToCart}
                  />
                } 
              />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
