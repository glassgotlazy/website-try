'use client';
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
  Trophy,
  Users,
  Target,
  Mail,
  Phone,
  MapPin,
  ChevronDown,
  Menu,
  X,
  Gamepad2,
  Zap,
  Award,
  Crown,
} from 'lucide-react';

export default function Home() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const scrollToSection = (sectionId: string) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
    setIsMenuOpen(false);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-red-900 to-black">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-black/80 backdrop-blur-md border-b border-red-500/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Gamepad2 className="w-8 h-8 text-red-500" />
              <span className="text-xl font-bold text-white tracking-wide">Elite Tatins</span>
            </div>

            {/* Desktop Menu */}
            <div className="hidden md:flex space-x-8">
              {['Home', 'Team', 'Achievements', 'About', 'Contact'].map((item) => (
                <button
                  key={item}
                  onClick={() => scrollToSection(item.toLowerCase())}
                  className="text-gray-300 hover:text-red-500 transition-colors duration-200"
                >
                  {item}
                </button>
              ))}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden text-white"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {isMenuOpen && (
            <div className="md:hidden bg-black/95 backdrop-blur-md absolute top-16 left-0 right-0 border-b border-red-500/30">
              <div className="px-4 py-4 space-y-3">
                {['Home', 'Team', 'Achievements', 'About', 'Contact'].map((item) => (
                  <button
                    key={item}
                    onClick={() => scrollToSection(item.toLowerCase())}
                    className="block w-full text-left text-gray-300 hover:text-red-500 transition-colors duration-200 py-2"
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="pt-16 min-h-screen flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-red-600/20 to-black/40" />
        <div
          className={`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10 transition-all duration-1000 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}
        >
          <div className="flex items-center justify-center mb-8">
            <Crown className="w-16 h-16 text-red-500 mr-4 animate-pulse" />
            <h1 className="text-6xl md:text-8xl font-extrabold text-white tracking-tight drop-shadow-lg">
              Elite <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-yellow-500">Tatins</span>
            </h1>
          </div>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto italic">
            Rising through the Call of Duty Mobile competitive scene with skill, passion, and tactical brilliance
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={() => scrollToSection('team')}
              size="lg"
              className="bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:shadow-red-500/50 transition-all duration-300"
            >
              <Users className="w-5 h-5 mr-2" />
              Meet the Team
            </Button>
            <Button
              onClick={() => scrollToSection('achievements')}
              variant="outline"
              size="lg"
              className="border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black px-8 py-3 rounded-xl font-bold transition-all duration-300"
            >
              <Trophy className="w-5 h-5 mr-2" />
              Our Journey
            </Button>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <ChevronDown className="w-6 h-6 text-red-400" />
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="py-20 bg-black/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              CODM <span className="text-red-500">Squad</span>
            </h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Meet the warriors carrying Elite Tatins' name in Call of Duty Mobile esports
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { name: 'Alex "Phoenix" Chen', role: 'IGL/Slayer', game: 'CODM', rank: 'Legendary' },
              { name: 'Sarah "Viper" Johnson', role: 'Assault/Entry', game: 'CODM', rank: 'Legendary' },
              { name: 'Mike "Thunder" Rodriguez', role: 'Support/Anchor', game: 'CODM', rank: 'Grand Master' },
              { name: 'Emma "Frost" Kim', role: 'Sniper/Flex', game: 'CODM', rank: 'Legendary' },
              { name: 'Jake "Storm" Wilson', role: 'Obj/Rusher', game: 'CODM', rank: 'Grand Master' },
              { name: 'Lisa "Nova" Zhang', role: 'Sub/Coach', game: 'CODM', rank: 'Master' },
            ].map((player, index) => (
              <Card
                key={index}
                className="bg-black/70 border border-red-600 hover:border-yellow-400 transition-all duration-300 hover:shadow-xl hover:shadow-red-500/20 group"
              >
                <CardContent className="p-6 text-center">
                  <div className="w-20 h-20 bg-gradient-to-br from-red-500 to-yellow-500 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Target className="w-10 h-10 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{player.name}</h3>
                  <p className="text-red-400 font-medium mb-1">{player.role}</p>
                  <p className="text-gray-400 text-sm mb-2">{player.game}</p>
                  <Badge variant="secondary" className="bg-yellow-500/20 text-yellow-400 border-yellow-500/30">
                    {player.rank}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Achievements Section */}
      <section id="achievements" className="py-20 bg-gradient-to-br from-black to-red-950">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Our <span className="text-yellow-400">Journey</span>
            </h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Building our legacy in Call of Duty Mobile competitive scene
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { tournament: 'CODM World Championship 2024', placement: '8th Place', prize: '$5,000', game: 'CODM' },
              { tournament: 'Regional Qualifiers', placement: '3rd Place', prize: '$2,500', game: 'CODM' },
              { tournament: 'Mobile Masters Cup', placement: '5th Place', prize: '$1,000', game: 'CODM' },
              { tournament: 'Elite Series Tournament', placement: '2nd Place', prize: '$3,000', game: 'CODM' },
              { tournament: 'Spring Championship', placement: '4th Place', prize: '$1,500', game: 'CODM' },
              { tournament: 'Local League Finals', placement: '1st Place', prize: '$800', game: 'CODM' },
            ].map((achievement, index) => (
              <Card
                key={index}
                className="bg-black/60 border border-red-600 hover:border-yellow-400 transition-all duration-300 hover:shadow-xl hover:shadow-yellow-500/20 group"
              >
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <Trophy className="w-8 h-8 text-yellow-400 group-hover:rotate-12 transition-transform duration-300" />
                    <Badge
                      variant="secondary"
                      className={`${
                        achievement.placement === '1st Place'
                          ? 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
                          : achievement.placement === '2nd Place'
                          ? 'bg-gray-400/20 text-gray-300 border-gray-400/30'
                          : 'bg-red-500/20 text-red-400 border-red-500/30'
                      }`}
                    >
                      {achievement.placement}
                    </Badge>
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">{achievement.tournament}</h3>
                  <p className="text-red-400 text-sm mb-2">{achievement.game}</p>
                  <p className="text-yellow-400 font-bold text-xl">{achievement.prize}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-black/70">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                About <span className="text-red-500">Elite Tatins</span>
              </h2>
              <p className="text-gray-300 text-lg mb-6 leading-relaxed">
                Founded in 2023, Elite Tatins is an ambitious Call of Duty Mobile esports organization focused on
                developing talent and competing at the highest levels. We're building our reputation through
                dedication, strategic gameplay, and continuous improvement.
              </p>
              <p className="text-gray-300 text-lg mb-8 leading-relaxed">
                As an upcoming organization, we're committed to growth, learning, and making our mark in the
                competitive CODM scene. Every match is an opportunity to prove ourselves and climb the ranks.
              </p>

              <div className="grid grid-cols-2 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-500 mb-2">15+</div>
                  <div className="text-gray-400">Tournaments Played</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-yellow-400 mb-2">$15K+</div>
                  <div className="text-gray-400">Prize Money</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-white mb-2">8</div>
                  <div className="text-gray-400">Active Players</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-red-300 mb-2">1</div>
                  <div className="text-gray-400">Main Title</div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-gradient-to-br from-red-600/30 to-black/40 p-8 rounded-2xl border border-red-600/50">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-black/50 p-4 rounded-lg text-center">
                    <Target className="w-8 h-8 text-red-400 mx-auto mb-2" />
                    <div className="text-white font-semibold">Aim</div>
                  </div>
                  <div className="bg-black/50 p-4 rounded-lg text-center">
                    <Zap className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                    <div className="text-white font-semibold">Speed</div>
                  </div>
                  <div className="bg-black/50 p-4 rounded-lg text-center">
                    <Users className="w-8 h-8 text-red-400 mx-auto mb-2" />
                    <div className="text-white font-semibold">Teamwork</div>
                  </div>
                  <div className="bg-black/50 p-4 rounded-lg text-center">
                    <Award className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                    <div className="text-white font-semibold">Growth</div>
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-white text-center">CODM Excellence</h3>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 bg-black/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Join the <span className="text-red-500">Elite</span>
            </h2>
            <p className="text-gray-300 text-lg max-w-2xl mx-auto">
              Ready to compete at the highest level? Get in touch with our management team
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            <div className="space-y-8">
              <div className="bg-black/60 p-6 rounded-lg border border-red-600">
                <h3 className="text-2xl font-bold text-white mb-4">Contact Information</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Mail className="w-5 h-5 text-red-400" />
                    <span className="text-gray-300">management@elitetatins.gg</span>
                  </div>
                  <
