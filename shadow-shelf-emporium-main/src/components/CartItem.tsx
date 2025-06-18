
import React from 'react';
import { Minus, Plus, Trash2 } from 'lucide-react';
import { Product } from './ProductCard';

export interface CartItemType extends Product {
  quantity: number;
}

interface CartItemProps {
  item: CartItemType;
  onUpdateQuantity: (id: number, quantity: number) => void;
  onRemove: (id: number) => void;
}

const CartItem = ({ item, onUpdateQuantity, onRemove }: CartItemProps) => {
  return (
    <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
      <div className="flex items-center space-x-4">
        <img
          src={item.image}
          alt={item.name}
          className="w-16 h-16 object-cover rounded-lg"
        />
        
        <div className="flex-1">
          <h3 className="text-white font-semibold">{item.name}</h3>
          <p className="text-gray-400 text-sm">{item.category}</p>
          <p className="text-purple-400 font-bold">${item.price}</p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => onUpdateQuantity(item.id, Math.max(0, item.quantity - 1))}
            className="p-1 bg-gray-800 hover:bg-gray-700 rounded text-gray-300 hover:text-white transition-colors"
          >
            <Minus className="w-4 h-4" />
          </button>
          <span className="text-white font-semibold w-8 text-center">{item.quantity}</span>
          <button
            onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
            className="p-1 bg-gray-800 hover:bg-gray-700 rounded text-gray-300 hover:text-white transition-colors"
          >
            <Plus className="w-4 h-4" />
          </button>
        </div>

        <button
          onClick={() => onRemove(item.id)}
          className="p-2 text-red-400 hover:text-red-300 hover:bg-red-900/20 rounded transition-colors"
        >
          <Trash2 className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default CartItem;
