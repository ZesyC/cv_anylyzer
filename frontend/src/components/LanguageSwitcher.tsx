/**
 * Language Switcher Component
 * Toggle button to switch between English and Vietnamese.
 */
import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const LanguageSwitcher: React.FC = () => {
  const { language, setLanguage } = useLanguage();

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'vi' : 'en');
  };

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-4 py-2 bg-white border-2 border-primary-500 rounded-lg hover:bg-primary-50 transition-colors font-medium text-primary-700"
      aria-label="Switch language"
    >
      <span className="text-xl">{language === 'en' ? '🇻🇳' : '🇬🇧'}</span>
      <span className="text-sm">{language === 'en' ? 'Tiếng Việt' : 'English'}</span>
    </button>
  );
};

export default LanguageSwitcher;
