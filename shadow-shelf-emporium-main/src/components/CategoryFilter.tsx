
import React from 'react';

interface CategoryFilterProps {
  categories: string[];
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const CategoryFilter = ({ categories, selectedCategory, onCategoryChange }: CategoryFilterProps) => {
  return (
    <div className="bg-gray-900 p-6 rounded-lg">
      <h3 className="text-white text-lg font-semibold mb-4">Categories</h3>
      <div className="space-y-2">
        <button
          onClick={() => onCategoryChange('all')}
          className={`w-full text-left px-4 py-2 rounded-lg transition-colors ${
            selectedCategory === 'all'
              ? 'bg-purple-600 text-white'
              : 'text-gray-300 hover:text-white hover:bg-gray-800'
          }`}
        >
          All Products
        </button>
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => onCategoryChange(category)}
            className={`w-full text-left px-4 py-2 rounded-lg transition-colors capitalize ${
              selectedCategory === category
                ? 'bg-purple-600 text-white'
                : 'text-gray-300 hover:text-white hover:bg-gray-800'
            }`}
          >
            {category}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CategoryFilter;
