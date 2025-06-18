
import React from 'react';
import ProductCard, { Product } from './ProductCard';

interface ProductGridProps {
  products: Product[];
  onAddToCart: (product: Product) => void;
  onProductClick: (product: Product) => void;
}

const ProductGrid = ({ products, onAddToCart, onProductClick }: ProductGridProps) => {
  if (products.length === 0) {
    return (
      <div className="col-span-full flex flex-col items-center justify-center py-12">
        <div className="text-gray-400 text-center">
          <h3 className="text-xl font-semibold mb-2">No products found</h3>
          <p>Try adjusting your search or filters</p>
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onAddToCart={onAddToCart}
          onProductClick={onProductClick}
        />
      ))}
    </div>
  );
};

export default ProductGrid;
